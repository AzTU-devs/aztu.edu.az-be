from typing import Optional

from fastapi import Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schema.honorary_doctor import (
    HonoraryDoctorCreate,
    HonoraryDoctorUpdate,
    ReOrderHonoraryDoctor,
)
from app.core.logger import get_logger
from app.core.session import get_db
from app.models.honorary.honorary_doctor import HonoraryDoctor
from app.models.honorary.honorary_doctor_tr import HonoraryDoctorTranslation
from app.utils.file_upload import ALLOWED_IMAGE_MIMES, safe_delete_file, save_upload
from app.utils.language import get_language

logger = get_logger(__name__)

UPLOAD_SUBDIRECTORY = "honorary_doctors"

LANGS = ("az", "en")


def _has_upload(upload) -> bool:
    """An omitted multipart part still arrives as an UploadFile with no filename."""
    return upload is not None and bool(getattr(upload, "filename", None))


def _serialize(doctor: HonoraryDoctor) -> dict:
    return {
        "id": doctor.id,
        "image": doctor.image,
        "display_order": doctor.display_order,
        "is_active": doctor.is_active,
    }


async def _next_display_order(db: AsyncSession) -> int:
    current_max = (await db.execute(select(func.max(HonoraryDoctor.display_order)))).scalar()
    return (current_max or 0) + 1


async def _translations_for(db: AsyncSession, doctor_id: int) -> dict:
    rows = (await db.execute(
        select(HonoraryDoctorTranslation).where(HonoraryDoctorTranslation.doctor_id == doctor_id)
    )).scalars().all()
    return {row.lang_code: row for row in rows}


async def _write_translations(db: AsyncSession, doctor_id: int, request) -> None:
    """Upsert both languages from one admin submission."""
    payload = {
        "az": (request.az_full_name, request.az_description),
        "en": (request.en_full_name, request.en_description),
    }
    existing = await _translations_for(db, doctor_id)
    for lang in LANGS:
        full_name, description = payload[lang]
        row = existing.get(lang)
        if row is None:
            db.add(HonoraryDoctorTranslation(
                doctor_id=doctor_id,
                lang_code=lang,
                full_name=full_name,
                description=description,
            ))
        else:
            row.full_name = full_name
            row.description = description


# ── Public read ────────────────────────────────────────────────────────────────

async def get_public_honorary_doctors(
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    """Active doctors in editor order, in one language.

    Returns 200 with an empty list rather than 204 when nothing is published, so
    the site can tell "loaded, none yet" apart from "request failed" and show a
    proper empty state instead of a spinner.
    """
    try:
        doctors = (await db.execute(
            select(HonoraryDoctor)
            .where(HonoraryDoctor.is_active.is_(True))
            .order_by(HonoraryDoctor.display_order.asc())
        )).scalars().all()

        result = []
        for doctor in doctors:
            translations = await _translations_for(db, doctor.id)
            tr = translations.get(lang) or translations.get("az")
            result.append({
                **_serialize(doctor),
                "full_name": tr.full_name if tr else None,
                "description": tr.description if tr else None,
            })

        return JSONResponse(content={
            "status_code": 200,
            "message": "Honorary doctors fetched successfully.",
            "total": len(result),
            "doctors": result,
        })
    except Exception:
        logger.exception("Failed to fetch public honorary doctors")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ── Admin read ─────────────────────────────────────────────────────────────────

async def get_honorary_doctors(
    start: int = Query(0, ge=0),
    end: int = Query(10, gt=0, le=100),
    db: AsyncSession = Depends(get_db),
):
    try:
        total = (await db.execute(select(func.count(HonoraryDoctor.id)))).scalar() or 0
        doctors = (await db.execute(
            select(HonoraryDoctor)
            .order_by(HonoraryDoctor.display_order.asc())
            .offset(start)
            .limit(max(end - start, 0))
        )).scalars().all()

        result = []
        for doctor in doctors:
            translations = await _translations_for(db, doctor.id)
            result.append({
                **_serialize(doctor),
                "az_full_name": translations["az"].full_name if "az" in translations else None,
                "en_full_name": translations["en"].full_name if "en" in translations else None,
                "az_description": translations["az"].description if "az" in translations else None,
                "en_description": translations["en"].description if "en" in translations else None,
            })

        return JSONResponse(content={
            "status_code": 200,
            "message": "Honorary doctors fetched successfully.",
            "total": total,
            "doctors": result,
        })
    except Exception:
        logger.exception("Failed to fetch honorary doctors")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def get_honorary_doctor_admin(doctor_id: int, db: AsyncSession = Depends(get_db)):
    try:
        doctor = (await db.execute(
            select(HonoraryDoctor).where(HonoraryDoctor.id == doctor_id)
        )).scalar_one_or_none()
        if doctor is None:
            return JSONResponse(
                content={"status_code": 404, "message": "Honorary doctor not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        translations = await _translations_for(db, doctor.id)
        return JSONResponse(content={
            "status_code": 200,
            "message": "Honorary doctor fetched successfully.",
            "doctor": {
                **_serialize(doctor),
                "az_full_name": translations["az"].full_name if "az" in translations else None,
                "en_full_name": translations["en"].full_name if "en" in translations else None,
                "az_description": translations["az"].description if "az" in translations else None,
                "en_description": translations["en"].description if "en" in translations else None,
            },
        })
    except Exception:
        logger.exception("Failed to fetch honorary doctor %s", doctor_id)
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ── Writes ─────────────────────────────────────────────────────────────────────

async def create_honorary_doctor(request: HonoraryDoctorCreate, db: AsyncSession = Depends(get_db)):
    saved_image: Optional[str] = None
    try:
        if _has_upload(request.image):
            saved_image = await save_upload(request.image, UPLOAD_SUBDIRECTORY, ALLOWED_IMAGE_MIMES)

        doctor = HonoraryDoctor(
            image=saved_image,
            display_order=await _next_display_order(db),
            is_active=True,
        )
        db.add(doctor)
        await db.flush()

        await _write_translations(db, doctor.id, request)
        await db.commit()

        return JSONResponse(content={
            "status_code": 201,
            "message": "Honorary doctor created successfully.",
            "id": doctor.id,
        }, status_code=status.HTTP_201_CREATED)
    except Exception:
        await db.rollback()
        # The row never landed, so the uploaded file would be orphaned.
        if saved_image:
            safe_delete_file(saved_image)
        logger.exception("Failed to create honorary doctor")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_honorary_doctor(
    doctor_id: int, request: HonoraryDoctorUpdate, db: AsyncSession = Depends(get_db)
):
    saved_image: Optional[str] = None
    try:
        doctor = (await db.execute(
            select(HonoraryDoctor).where(HonoraryDoctor.id == doctor_id)
        )).scalar_one_or_none()
        if doctor is None:
            return JSONResponse(
                content={"status_code": 404, "message": "Honorary doctor not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        previous_image = doctor.image
        if _has_upload(request.image):
            saved_image = await save_upload(request.image, UPLOAD_SUBDIRECTORY, ALLOWED_IMAGE_MIMES)
            doctor.image = saved_image
        elif request.remove_image:
            doctor.image = None

        await _write_translations(db, doctor.id, request)
        await db.commit()

        # Only drop the old file once the new state is committed.
        if previous_image and previous_image != doctor.image:
            safe_delete_file(previous_image)

        return JSONResponse(content={
            "status_code": 200,
            "message": "Honorary doctor updated successfully.",
        })
    except Exception:
        await db.rollback()
        if saved_image:
            safe_delete_file(saved_image)
        logger.exception("Failed to update honorary doctor %s", doctor_id)
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def reorder_honorary_doctor(request: ReOrderHonoraryDoctor, db: AsyncSession = Depends(get_db)):
    try:
        for position, doctor_id in enumerate(request.ids, start=1):
            doctor = (await db.execute(
                select(HonoraryDoctor).where(HonoraryDoctor.id == doctor_id)
            )).scalar_one_or_none()
            if doctor is not None:
                doctor.display_order = position
        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "Order updated successfully."})
    except Exception:
        await db.rollback()
        logger.exception("Failed to reorder honorary doctors")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def _set_active(doctor_id: int, value: bool, db: AsyncSession):
    try:
        doctor = (await db.execute(
            select(HonoraryDoctor).where(HonoraryDoctor.id == doctor_id)
        )).scalar_one_or_none()
        if doctor is None:
            return JSONResponse(
                content={"status_code": 404, "message": "Honorary doctor not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        doctor.is_active = value
        await db.commit()
        return JSONResponse(content={
            "status_code": 200,
            "message": "Honorary doctor published." if value else "Honorary doctor unpublished.",
            "is_active": value,
        })
    except Exception:
        await db.rollback()
        logger.exception("Failed to change honorary doctor %s state", doctor_id)
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def activate_honorary_doctor(doctor_id: int, db: AsyncSession = Depends(get_db)):
    return await _set_active(doctor_id, True, db)


async def deactivate_honorary_doctor(doctor_id: int, db: AsyncSession = Depends(get_db)):
    return await _set_active(doctor_id, False, db)


async def delete_honorary_doctor(doctor_id: int, db: AsyncSession = Depends(get_db)):
    try:
        doctor = (await db.execute(
            select(HonoraryDoctor).where(HonoraryDoctor.id == doctor_id)
        )).scalar_one_or_none()
        if doctor is None:
            return JSONResponse(
                content={"status_code": 404, "message": "Honorary doctor not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        image = doctor.image
        await db.execute(
            sqlalchemy_delete(HonoraryDoctorTranslation).where(
                HonoraryDoctorTranslation.doctor_id == doctor_id
            )
        )
        await db.execute(sqlalchemy_delete(HonoraryDoctor).where(HonoraryDoctor.id == doctor_id))
        await db.commit()

        if image:
            safe_delete_file(image)

        return JSONResponse(content={"status_code": 200, "message": "Honorary doctor deleted successfully."})
    except Exception:
        await db.rollback()
        logger.exception("Failed to delete honorary doctor %s", doctor_id)
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
