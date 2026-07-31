import secrets
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import select, func, delete as sqlalchemy_delete
from app.core.session import get_db
from app.core.logger import get_logger

logger = get_logger(__name__)

from app.api.v1.schema.hero_certificate import *
from fastapi import Depends, status, Query, HTTPException
from fastapi.responses import JSONResponse
from app.utils.language import get_language
from app.utils.file_upload import save_upload, safe_delete_file, ALLOWED_IMAGE_MIMES, ALLOWED_DOC_MIMES
from app.models.hero_certificate.hero_certificate import HeroCertificate
from app.models.hero_certificate.hero_certificate_tr import HeroCertificateTranslation
from sqlalchemy.ext.asyncio import AsyncSession


ALLOWED_FAMILIES = ("world", "europe", "subject", "other")

UPLOAD_SUBDIRECTORY = "hero_certificates"

_TR_FIELDS = ("title", "kicker", "signer")


def hero_certificate_id_generator() -> int:
    return secrets.randbelow(900000) + 100000


def _has_upload(upload) -> bool:
    """An omitted multipart part still arrives as an UploadFile with no filename."""
    return upload is not None and bool(getattr(upload, "filename", None))


def _normalise_family(family: Optional[str]) -> Optional[str]:
    if not isinstance(family, str):
        return None
    family = family.strip().lower()
    return family if family in ALLOWED_FAMILIES else None


def _missing_source_response() -> JSONResponse:
    return JSONResponse(
        content={
            "status_code": 422,
            "message": "A certificate needs at least one of: image, document or external_url."
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


def _invalid_family_response() -> JSONResponse:
    return JSONResponse(
        content={
            "status_code": 422,
            "message": f"Invalid family. Expected one of: {', '.join(ALLOWED_FAMILIES)}."
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


def _serialize(certificate: HeroCertificate) -> dict:
    return {
        "id": certificate.id,
        "certificate_id": certificate.certificate_id,
        "rank_label": certificate.rank_label,
        "family": certificate.family,
        "image": certificate.image,
        "document": certificate.document,
        "external_url": certificate.external_url,
        "issued_date": certificate.issued_date.isoformat() if certificate.issued_date else None,
        "display_order": certificate.display_order,
        "is_active": certificate.is_active,
        "created_at": certificate.created_at.isoformat() if certificate.created_at else None,
        "updated_at": certificate.updated_at.isoformat() if certificate.updated_at else None,
    }


def _resequence_display_order(rows: list, target, new_order: int) -> None:
    """Move `target` to position `new_order` (1-based) within `rows` and renumber 1..N.

    `rows` must already be ordered by current display_order. Mutates display_order in
    place; clamps out-of-range positions to the valid [1, total] window.
    """
    total = len(rows)
    if total == 0:
        return
    new_order = max(1, min(int(new_order), total))
    ordered = [r for r in rows if r is not target]
    ordered.insert(new_order - 1, target)
    for idx, r in enumerate(ordered, start=1):
        if r.display_order != idx:
            r.display_order = idx


async def create_hero_certificate(
    request: HeroCertificateCreate,
    db: AsyncSession = Depends(get_db),
):
    saved_files: list[str] = []
    try:
        family = _normalise_family(request.family)
        if family is None:
            return _invalid_family_response()

        has_image = _has_upload(request.image)
        has_document = _has_upload(request.document)

        # BUSINESS RULE: at least one of image / document / external_url.
        # Checked before anything is written to disk so a rejected request
        # leaves no orphan uploads behind.
        if not (has_image or has_document or request.external_url):
            return _missing_source_response()

        certificate_id = hero_certificate_id_generator()

        image_path: Optional[str] = None
        document_path: Optional[str] = None

        if has_image:
            image_path = await save_upload(request.image, UPLOAD_SUBDIRECTORY, ALLOWED_IMAGE_MIMES)
            saved_files.append(image_path)

        if has_document:
            document_path = await save_upload(
                request.document,
                UPLOAD_SUBDIRECTORY,
                ALLOWED_DOC_MIMES,
                allow_extension_fallback=True,
            )
            saved_files.append(document_path)

        for item in (await db.execute(select(HeroCertificate))).scalars().all():
            item.display_order = (item.display_order or 0) + 1
            db.add(item)

        db.add(HeroCertificate(
            certificate_id=certificate_id,
            rank_label=request.rank_label,
            family=family,
            image=image_path,
            document=document_path,
            external_url=request.external_url,
            issued_date=request.issued_date,
            display_order=1,
            is_active=True,
            created_at=datetime.now(timezone.utc)
        ))
        db.add(HeroCertificateTranslation(
            certificate_id=certificate_id,
            lang_code="az",
            title=request.az.title,
            kicker=request.az.kicker,
            signer=request.az.signer
        ))
        db.add(HeroCertificateTranslation(
            certificate_id=certificate_id,
            lang_code="en",
            title=request.en.title,
            kicker=request.en.kicker,
            signer=request.en.signer
        ))
        await db.commit()

        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Hero certificate created successfully.",
                "certificate_id": certificate_id
            },
            status_code=status.HTTP_201_CREATED
        )

    except HTTPException:
        # save_upload raises 413/415 — let those reach the client instead of
        # being flattened into a generic 500.
        await db.rollback()
        for f in saved_files:
            safe_delete_file(f)
        raise
    except Exception:
        await db.rollback()
        for f in saved_files:
            safe_delete_file(f)
        logger.exception("Failed to create hero certificate")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def get_public_hero_certificates(
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        certificates = (await db.execute(
            select(HeroCertificate)
            .where(HeroCertificate.is_active.is_(True))
            .order_by(HeroCertificate.display_order.asc())
        )).scalars().all()

        if not certificates:
            return JSONResponse(
                content={"status_code": 204, "message": "No content."},
                status_code=status.HTTP_204_NO_CONTENT
            )

        result_arr = []
        for certificate in certificates:
            tr = (await db.execute(
                select(HeroCertificateTranslation).where(
                    HeroCertificateTranslation.certificate_id == certificate.certificate_id,
                    HeroCertificateTranslation.lang_code == lang
                )
            )).scalar_one_or_none()
            result_arr.append({
                **_serialize(certificate),
                "title": tr.title if tr else None,
                "kicker": tr.kicker if tr else None,
                "signer": tr.signer if tr else None,
            })

        return JSONResponse(content={
            "status_code": 200,
            "message": "Hero certificates fetched successfully.",
            "total": len(result_arr),
            "certificates": result_arr
        })

    except Exception:
        logger.exception("Failed to fetch public hero certificates")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def get_hero_certificates(
    start: int = Query(0, ge=0),
    end: int = Query(10, gt=0, le=100),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    try:
        total = (await db.execute(select(func.count()).select_from(HeroCertificate))).scalar() or 0

        # `end` is an index, not a count. Clamp so that end <= start yields an
        # empty page instead of "LIMIT must not be negative" (a 500).
        limit = max(0, end - start)

        certificates = (await db.execute(
            select(HeroCertificate)
            .order_by(HeroCertificate.display_order.asc())
            .offset(start)
            .limit(limit)
        )).scalars().all()

        if not certificates:
            return JSONResponse(
                content={"status_code": 204, "message": "No content."},
                status_code=status.HTTP_204_NO_CONTENT
            )

        result_arr = []
        for certificate in certificates:
            tr = (await db.execute(
                select(HeroCertificateTranslation).where(
                    HeroCertificateTranslation.certificate_id == certificate.certificate_id,
                    HeroCertificateTranslation.lang_code == lang
                )
            )).scalar_one_or_none()
            result_arr.append({
                **_serialize(certificate),
                "title": tr.title if tr else None,
                "kicker": tr.kicker if tr else None,
                "signer": tr.signer if tr else None,
            })

        return JSONResponse(content={
            "status_code": 200,
            "message": "Hero certificates fetched successfully.",
            "total": total,
            "certificates": result_arr
        })

    except Exception:
        logger.exception("Failed to fetch hero certificates")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def get_hero_certificate_admin(
    certificate_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        certificate = (await db.execute(
            select(HeroCertificate).where(HeroCertificate.certificate_id == certificate_id)
        )).scalar_one_or_none()
        if not certificate:
            return JSONResponse(
                content={"status_code": 404, "message": "Hero certificate not found."},
                status_code=status.HTTP_404_NOT_FOUND
            )

        translations = (await db.execute(
            select(HeroCertificateTranslation).where(
                HeroCertificateTranslation.certificate_id == certificate_id
            )
        )).scalars().all()
        by_lang = {tr.lang_code: tr for tr in translations}

        def _translation(lang_code: str) -> dict:
            tr = by_lang.get(lang_code)
            return {field: (getattr(tr, field) if tr else None) or "" for field in _TR_FIELDS}

        return JSONResponse(content={
            "status_code": 200,
            "message": "Hero certificate fetched successfully.",
            "certificate": {
                **_serialize(certificate),
                "az": _translation("az"),
                "en": _translation("en"),
            }
        })

    except Exception:
        logger.exception("Failed to fetch hero certificate admin detail")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def update_hero_certificate(
    certificate_id: int,
    request: HeroCertificateUpdate,
    db: AsyncSession = Depends(get_db)
):
    saved_files: list[str] = []
    try:
        certificate = (await db.execute(
            select(HeroCertificate).where(HeroCertificate.certificate_id == certificate_id)
        )).scalar_one_or_none()
        if not certificate:
            return JSONResponse(
                content={"status_code": 404, "message": "Hero certificate not found."},
                status_code=status.HTTP_404_NOT_FOUND
            )

        family = _normalise_family(request.family)
        if family is None:
            return _invalid_family_response()

        has_image = _has_upload(request.image)
        has_document = _has_upload(request.document)

        # A new upload always wins over the corresponding remove_* flag.
        keeps_image = has_image or (bool(certificate.image) and not request.remove_image)
        keeps_document = has_document or (bool(certificate.document) and not request.remove_document)

        # BUSINESS RULE: the record must not end up with none of the three sources.
        if not (keeps_image or keeps_document or request.external_url):
            return _missing_source_response()

        old_image: Optional[str] = None
        old_document: Optional[str] = None

        if has_image:
            new_image_path = await save_upload(request.image, UPLOAD_SUBDIRECTORY, ALLOWED_IMAGE_MIMES)
            saved_files.append(new_image_path)
            old_image = certificate.image
            certificate.image = new_image_path
        elif request.remove_image:
            old_image = certificate.image
            certificate.image = None

        if has_document:
            new_document_path = await save_upload(
                request.document,
                UPLOAD_SUBDIRECTORY,
                ALLOWED_DOC_MIMES,
                allow_extension_fallback=True,
            )
            saved_files.append(new_document_path)
            old_document = certificate.document
            certificate.document = new_document_path
        elif request.remove_document:
            old_document = certificate.document
            certificate.document = None

        certificate.rank_label = request.rank_label
        certificate.family = family
        certificate.external_url = request.external_url
        certificate.issued_date = request.issued_date
        certificate.updated_at = datetime.now(timezone.utc)

        db.add(certificate)

        translations = (await db.execute(
            select(HeroCertificateTranslation).where(
                HeroCertificateTranslation.certificate_id == certificate_id
            )
        )).scalars().all()
        tr_by_lang = {tr.lang_code: tr for tr in translations}

        for lang_code, form in [("az", request.az), ("en", request.en)]:
            tr = tr_by_lang.get(lang_code)
            if tr is None:
                # Upsert: a language row created after the fact (or missing from a
                # legacy record) is inserted rather than silently skipped.
                db.add(HeroCertificateTranslation(
                    certificate_id=certificate_id,
                    lang_code=lang_code,
                    title=form.title,
                    kicker=form.kicker,
                    signer=form.signer
                ))
                continue
            tr.title = form.title
            tr.kicker = form.kicker
            tr.signer = form.signer
            db.add(tr)

        await db.commit()

        # Old files are removed only after a successful commit.
        if old_image:
            safe_delete_file(old_image)
        if old_document:
            safe_delete_file(old_document)

        return JSONResponse(content={
            "status_code": 200,
            "message": "Hero certificate updated successfully."
        })

    except HTTPException:
        await db.rollback()
        for f in saved_files:
            safe_delete_file(f)
        raise
    except Exception:
        await db.rollback()
        for f in saved_files:
            safe_delete_file(f)
        logger.exception("Failed to update hero certificate")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def reorder_hero_certificate(
    request: ReOrderHeroCertificate,
    db: AsyncSession = Depends(get_db)
):
    try:
        all_rows = (await db.execute(
            select(HeroCertificate)
            .order_by(HeroCertificate.display_order.asc(), HeroCertificate.created_at.desc())
            .with_for_update()
        )).scalars().all()

        target = next((c for c in all_rows if c.certificate_id == request.certificate_id), None)
        if not target:
            return JSONResponse(content={"status_code": 404, "error": "Hero certificate not found"}, status_code=404)

        _resequence_display_order(all_rows, target, request.new_order)

        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "Hero certificate reordered successfully"})

    except Exception:
        await db.rollback()
        logger.exception("Failed to reorder hero certificate")
        return JSONResponse(content={"status_code": 500, "error": "Internal server error"}, status_code=500)


async def activate_hero_certificate(
    certificate_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        certificate = (await db.execute(
            select(HeroCertificate).where(HeroCertificate.certificate_id == certificate_id)
        )).scalars().first()
        if not certificate:
            return JSONResponse(
                content={"status_code": 404, "message": "Hero certificate not found."},
                status_code=status.HTTP_404_NOT_FOUND
            )

        certificate.is_active = True
        await db.commit()

        return JSONResponse(content={"status_code": 200, "message": "Hero certificate activated successfully."})

    except Exception:
        await db.rollback()
        logger.exception("Failed to activate hero certificate")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def deactivate_hero_certificate(
    certificate_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        certificate = (await db.execute(
            select(HeroCertificate).where(HeroCertificate.certificate_id == certificate_id)
        )).scalars().first()
        if not certificate:
            return JSONResponse(
                content={"status_code": 404, "message": "Hero certificate not found."},
                status_code=status.HTTP_404_NOT_FOUND
            )

        certificate.is_active = False
        await db.commit()

        return JSONResponse(content={"status_code": 200, "message": "Hero certificate deactivated successfully."})

    except Exception:
        await db.rollback()
        logger.exception("Failed to deactivate hero certificate")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def delete_hero_certificate(
    certificate_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        certificate = (await db.execute(
            select(HeroCertificate).where(HeroCertificate.certificate_id == certificate_id)
        )).scalar_one_or_none()
        if not certificate:
            return JSONResponse(
                content={"status_code": 404, "message": "Hero certificate not found."},
                status_code=status.HTTP_404_NOT_FOUND
            )

        image_path = certificate.image
        document_path = certificate.document

        await db.execute(sqlalchemy_delete(HeroCertificateTranslation).where(
            HeroCertificateTranslation.certificate_id == certificate_id
        ))
        await db.execute(sqlalchemy_delete(HeroCertificate).where(
            HeroCertificate.certificate_id == certificate_id
        ))

        # Close the hole the delete just left. Without this the surviving rows
        # keep their old numbers (1, 3, 4 …), the dashboard's "Sıra" column stops
        # matching the row's actual position, and the reorder dialog pre-fills a
        # number the API then has to clamp.
        remaining = (await db.execute(
            select(HeroCertificate).order_by(
                HeroCertificate.display_order.asc(), HeroCertificate.created_at.desc()
            )
        )).scalars().all()
        for idx, row in enumerate(remaining, start=1):
            if row.display_order != idx:
                row.display_order = idx

        await db.commit()

        if image_path:
            safe_delete_file(image_path)
        if document_path:
            safe_delete_file(document_path)

        return JSONResponse(content={"status_code": 200, "message": "Hero certificate deleted successfully."})

    except Exception:
        await db.rollback()
        logger.exception("Failed to delete hero certificate")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
