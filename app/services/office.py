"""Offices & Centres service.

An office is created from its name alone — which mints the az/en slugs — and
then edited as one whole document, the way the About pages save: the nested
collections (core functions, the director's education history, staff) arrive
whole and replace what is stored. Two read shapes:

* ``get_office_admin`` returns both languages side by side plus every id.
* ``get_office_public`` resolves one language, refuses unpublished offices, and
  is addressed by slug — it is what the website consumes.
"""

from datetime import datetime, timezone
from typing import Any, Iterable, Optional

from fastapi import HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete as sqlalchemy_delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.v1.schema.office import OfficeCreate, UpdateOffice
from app.core.logger import get_logger
from app.models.office.office import (
    Office,
    OfficeTr,
    OfficeFunction,
    OfficeFunctionTr,
    OfficeEducation,
    OfficeEducationTr,
    OfficeStaff,
    OfficeStaffTr,
)
from app.utils.file_upload import ALLOWED_IMAGE_MIMES, safe_delete_file, save_upload
from app.utils.html_sanitizer import sanitize_html
from app.utils.slug import make_slug

logger = get_logger(__name__)

LANGS = ("az", "en")

OFFICE_FIELDS = (
    "director_phone", "director_phone_code", "director_email", "director_image_url",
    "contact_phone", "contact_phone_code", "contact_email",
)
OFFICE_TR_FIELDS = (
    "name", "short_description", "about_title", "about_text", "goal_title", "goals",
    "functions_title", "director_title", "director_name", "director_surname",
    "director_position", "director_bio", "director_room", "director_work_hours",
    "staff_title", "contact_room", "contact_work_hours",
)
FUNCTION_TR_FIELDS = ("title", "description")
EDUCATION_FIELDS = ("start_year", "end_year")
EDUCATION_TR_FIELDS = ("degree", "university")
STAFF_FIELDS = ("phone", "phone_code", "email", "image_url")
STAFF_TR_FIELDS = ("name", "surname", "duty")

# Editor-authored HTML, scrubbed on the way in.
RICH_TEXT_FIELDS = frozenset({"short_description", "about_text", "director_bio", "description"})


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _error(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(
        content={"status_code": status_code, "message": message}, status_code=status_code
    )


def _apply(target: Any, data: dict, fields: Iterable[str]) -> None:
    """Copy only the keys the caller actually sent (PATCH semantics)."""
    for field in fields:
        if field not in data:
            continue
        value = data[field]
        if field in RICH_TEXT_FIELDS and isinstance(value, str):
            value = sanitize_html(value)
        setattr(target, field, value)


async def _upsert_translations(
    db: AsyncSession,
    model: Any,
    fk_name: str,
    fk_value: int,
    payload: dict,
    fields: Iterable[str],
    now: datetime,
) -> None:
    """Writes the az/en rows for one parent, creating whichever is missing."""
    for lang in LANGS:
        tr_data = payload.get(lang)
        if tr_data is None:
            continue
        existing = (
            await db.execute(
                select(model).where(
                    getattr(model, fk_name) == fk_value, model.lang_code == lang
                )
            )
        ).scalar_one_or_none()
        if existing is None:
            existing = model(
                **{fk_name: fk_value}, lang_code=lang, created_at=now, updated_at=now
            )
            db.add(existing)
        _apply(existing, tr_data, fields)
        existing.updated_at = now


def _tr_map(translations: Iterable[Any], fields: Iterable[str]) -> dict:
    """`{az: {...}, en: {...}}`, blank for a language never authored."""
    by_lang = {tr.lang_code: tr for tr in translations}
    return {
        lang: {f: (getattr(by_lang[lang], f) if lang in by_lang else None) for f in fields}
        for lang in LANGS
    }


def _pick(translations: Iterable[Any], lang: str, fields: Iterable[str]) -> dict:
    """One language's values, falling back to the other so a half-filled office still renders."""
    by_lang = {tr.lang_code: tr for tr in translations}
    primary = by_lang.get(lang)
    fallback = by_lang.get("az" if lang == "en" else "en")
    out = {}
    for field in fields:
        value = getattr(primary, field, None) if primary else None
        if value is None or (isinstance(value, str) and value.strip() == ""):
            value = getattr(fallback, field, None) if fallback else None
        out[field] = value
    return out


async def _unique_slug(db: AsyncSession, base: str, column: str) -> str:
    """A slug not yet used by another office, suffixing -2, -3 … on collision."""
    base = base or "ofis"
    col = getattr(Office, column)
    candidate = base
    suffix = 2
    while (
        await db.execute(select(Office.id).where(col == candidate))
    ).scalar_one_or_none() is not None:
        candidate = f"{base}-{suffix}"
        suffix += 1
    return candidate


# ── Loading ──────────────────────────────────────────────────────────────────


def _office_query():
    return select(Office).options(
        selectinload(Office.translations),
        selectinload(Office.functions).selectinload(OfficeFunction.translations),
        selectinload(Office.educations).selectinload(OfficeEducation.translations),
        selectinload(Office.staff).selectinload(OfficeStaff.translations),
    )


async def _load_by_id(db: AsyncSession, office_id: int) -> Optional[Office]:
    result = await db.execute(_office_query().where(Office.id == office_id))
    return result.scalars().unique().one_or_none()


async def _load_by_slug(db: AsyncSession, slug: str) -> Optional[Office]:
    result = await db.execute(
        _office_query().where((Office.slug_az == slug) | (Office.slug_en == slug))
    )
    return result.scalars().unique().one_or_none()


def _serialize_admin(office: Office) -> dict:
    return {
        "id": office.id,
        "slug_az": office.slug_az,
        "slug_en": office.slug_en,
        "display_order": office.display_order,
        "is_active": office.is_active,
        **{field: getattr(office, field) for field in OFFICE_FIELDS},
        **_tr_map(office.translations, OFFICE_TR_FIELDS),
        "functions": [
            {
                "id": fn.id,
                "display_order": fn.display_order,
                **_tr_map(fn.translations, FUNCTION_TR_FIELDS),
            }
            for fn in sorted(office.functions, key=lambda x: x.display_order)
        ],
        "educations": [
            {
                "id": edu.id,
                "display_order": edu.display_order,
                **{field: getattr(edu, field) for field in EDUCATION_FIELDS},
                **_tr_map(edu.translations, EDUCATION_TR_FIELDS),
            }
            for edu in sorted(office.educations, key=lambda x: x.display_order)
        ],
        "staff": [
            {
                "id": member.id,
                "display_order": member.display_order,
                **{field: getattr(member, field) for field in STAFF_FIELDS},
                **_tr_map(member.translations, STAFF_TR_FIELDS),
            }
            for member in sorted(office.staff, key=lambda x: x.display_order)
        ],
        "updated_at": office.updated_at.isoformat() if office.updated_at else None,
    }


def _serialize_public(office: Office, lang: str) -> dict:
    return {
        "slug": office.slug_az if lang == "az" else office.slug_en,
        **{field: getattr(office, field) for field in OFFICE_FIELDS},
        **_pick(office.translations, lang, OFFICE_TR_FIELDS),
        "functions": [
            _pick(fn.translations, lang, FUNCTION_TR_FIELDS)
            for fn in sorted(office.functions, key=lambda x: x.display_order)
        ],
        "educations": [
            {
                **{field: getattr(edu, field) for field in EDUCATION_FIELDS},
                **_pick(edu.translations, lang, EDUCATION_TR_FIELDS),
            }
            for edu in sorted(office.educations, key=lambda x: x.display_order)
        ],
        "staff": [
            {
                **{field: getattr(member, field) for field in STAFF_FIELDS},
                **_pick(member.translations, lang, STAFF_TR_FIELDS),
            }
            for member in sorted(office.staff, key=lambda x: x.display_order)
        ],
    }


# ── Reads ────────────────────────────────────────────────────────────────────


async def get_offices_admin(db: AsyncSession):
    """The list screen — every office, drafts included."""
    try:
        result = await db.execute(
            _office_query().order_by(Office.display_order, Office.id)
        )
        offices = result.scalars().unique().all()
        payload = [
            {
                "id": office.id,
                "slug_az": office.slug_az,
                "slug_en": office.slug_en,
                "is_active": office.is_active,
                "name_az": _tr_map(office.translations, ("name",))["az"]["name"],
                "name_en": _tr_map(office.translations, ("name",))["en"]["name"],
                "updated_at": office.updated_at.isoformat() if office.updated_at else None,
            }
            for office in offices
        ]
        return JSONResponse(content={"status_code": 200, "offices": payload})
    except Exception:
        logger.exception("Failed to list offices")
        return _error(500, "Failed to list offices.")


async def get_office_admin(office_id: int, db: AsyncSession):
    try:
        office = await _load_by_id(db, office_id)
        if office is None:
            return _error(404, "Office not found.")
        return JSONResponse(content={"status_code": 200, "office": _serialize_admin(office)})
    except Exception:
        logger.exception("Failed to load office %s", office_id)
        return _error(500, "Failed to load office.")


async def get_offices_public(lang: str, db: AsyncSession):
    """Published offices only, one language — for the website's list/grid."""
    try:
        result = await db.execute(
            _office_query()
            .where(Office.is_active.is_(True))
            .order_by(Office.display_order, Office.id)
        )
        offices = result.scalars().unique().all()
        payload = [
            {
                "slug": office.slug_az if lang == "az" else office.slug_en,
                **_pick(office.translations, lang, ("name", "short_description")),
            }
            for office in offices
        ]
        return JSONResponse(content={"status_code": 200, "offices": payload})
    except Exception:
        logger.exception("Failed to list public offices")
        return _error(500, "Failed to list offices.")


async def get_office_public(slug: str, lang: str, db: AsyncSession):
    try:
        office = await _load_by_slug(db, slug)
        if office is None or not office.is_active:
            return _error(404, "Office not found.")
        return JSONResponse(
            content={"status_code": 200, "office": _serialize_public(office, lang)}
        )
    except Exception:
        logger.exception("Failed to load public office %s", slug)
        return _error(500, "Failed to load office.")


# ── Writes ───────────────────────────────────────────────────────────────────


async def create_office(request: OfficeCreate, db: AsyncSession):
    """Creates a draft office from its name and mints the az/en slugs."""
    try:
        name_az = (request.name_az or "").strip()
        name_en = (request.name_en or "").strip()
        if not name_az and not name_en:
            return _error(422, "A name in at least one language is required.")

        now = _now()
        slug_az = await _unique_slug(db, make_slug(name_az or name_en), "slug_az")
        slug_en = await _unique_slug(db, make_slug(name_en or name_az), "slug_en")

        next_order = (
            await db.execute(select(func.coalesce(func.max(Office.display_order), -1)))
        ).scalar_one() + 1

        office = Office(
            slug_az=slug_az,
            slug_en=slug_en,
            display_order=next_order,
            is_active=False,
            created_at=now,
            updated_at=now,
        )
        db.add(office)
        await db.flush()

        db.add(OfficeTr(office_id=office.id, lang_code="az", name=name_az or name_en, created_at=now, updated_at=now))
        db.add(OfficeTr(office_id=office.id, lang_code="en", name=name_en or name_az, created_at=now, updated_at=now))

        await db.commit()
        return JSONResponse(
            content={
                "status_code": 201,
                "message": "Office created.",
                "data": {"id": office.id, "slug_az": slug_az, "slug_en": slug_en},
            },
            status_code=201,
        )
    except Exception:
        await db.rollback()
        logger.exception("Failed to create office")
        return _error(500, "Failed to create office.")


async def _replace_functions(db: AsyncSession, office_id: int, functions: list, now: datetime):
    """Rewrites the core-function cards wholesale — position is identity."""
    await db.execute(
        sqlalchemy_delete(OfficeFunction).where(OfficeFunction.office_id == office_id)
    )
    for index, entry in enumerate(functions):
        payload = entry if isinstance(entry, dict) else entry.dict(exclude_unset=True)
        fn = OfficeFunction(office_id=office_id, display_order=index, created_at=now, updated_at=now)
        db.add(fn)
        await db.flush()
        await _upsert_translations(
            db, OfficeFunctionTr, "function_id", fn.id, payload, FUNCTION_TR_FIELDS, now
        )


async def _replace_educations(db: AsyncSession, office_id: int, educations: list, now: datetime):
    """Rewrites the director's education history wholesale. Order is meaningful
    (the dashboard sends it PhD → Bachelor)."""
    await db.execute(
        sqlalchemy_delete(OfficeEducation).where(OfficeEducation.office_id == office_id)
    )
    for index, entry in enumerate(educations):
        payload = entry if isinstance(entry, dict) else entry.dict(exclude_unset=True)
        edu = OfficeEducation(office_id=office_id, display_order=index, created_at=now, updated_at=now)
        _apply(edu, payload, EDUCATION_FIELDS)
        db.add(edu)
        await db.flush()
        await _upsert_translations(
            db, OfficeEducationTr, "education_id", edu.id, payload, EDUCATION_TR_FIELDS, now
        )


async def _replace_staff(db: AsyncSession, office_id: int, staff: list, now: datetime):
    """Rewrites the staff roster wholesale. Any stored photo dropped from the
    roster is removed from disk; a pasted URL is left alone."""
    kept: set[str] = set()
    rows = []
    for index, entry in enumerate(staff):
        payload = entry if isinstance(entry, dict) else entry.dict(exclude_unset=True)
        image = (payload.get("image_url") or "").strip()
        kept.add(image)
        rows.append((index, payload))

    previous = (
        await db.execute(select(OfficeStaff).where(OfficeStaff.office_id == office_id))
    ).scalars().all()
    orphans = [
        member.image_url
        for member in previous
        if member.image_url
        and member.image_url not in kept
        and not member.image_url.startswith(("http://", "https://"))
    ]

    await db.execute(sqlalchemy_delete(OfficeStaff).where(OfficeStaff.office_id == office_id))
    for index, payload in rows:
        member = OfficeStaff(office_id=office_id, display_order=index, created_at=now, updated_at=now)
        _apply(member, payload, STAFF_FIELDS)
        db.add(member)
        await db.flush()
        await _upsert_translations(
            db, OfficeStaffTr, "staff_id", member.id, payload, STAFF_TR_FIELDS, now
        )

    for path in orphans:
        safe_delete_file(path)


async def update_office(office_id: int, request: UpdateOffice, db: AsyncSession):
    try:
        office = (
            await db.execute(select(Office).where(Office.id == office_id))
        ).scalar_one_or_none()
        if office is None:
            return _error(404, "Office not found.")

        now = _now()
        data = request.dict(exclude_unset=True)

        # Replacing the director's portrait with a different stored file orphans
        # the old one — clean it up, but never touch a pasted URL.
        if "director_image_url" in data:
            previous = office.director_image_url
            new = data["director_image_url"]
            if previous and previous != new and not previous.startswith(("http://", "https://")):
                safe_delete_file(previous)

        for field in OFFICE_FIELDS:
            if field in data:
                setattr(office, field, data[field])
        office.updated_at = now

        await _upsert_translations(
            db, OfficeTr, "office_id", office.id, data, OFFICE_TR_FIELDS, now
        )

        if data.get("functions") is not None:
            await _replace_functions(db, office.id, data["functions"], now)
        if data.get("educations") is not None:
            await _replace_educations(db, office.id, data["educations"], now)
        if data.get("staff") is not None:
            await _replace_staff(db, office.id, data["staff"], now)

        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "Office updated."})
    except Exception:
        await db.rollback()
        logger.exception("Failed to update office %s", office_id)
        return _error(500, "Failed to update office.")


async def publish_office(office_id: int, is_active: bool, db: AsyncSession):
    """The only way an office goes live, so saving a draft can never publish it."""
    try:
        office = (
            await db.execute(select(Office).where(Office.id == office_id))
        ).scalar_one_or_none()
        if office is None:
            return _error(404, "Office not found.")
        office.is_active = is_active
        office.updated_at = _now()
        await db.commit()
        return JSONResponse(
            content={
                "status_code": status.HTTP_200_OK,
                "message": "Office published." if is_active else "Office unpublished.",
                "is_active": is_active,
            }
        )
    except Exception:
        await db.rollback()
        logger.exception("Failed to change publication state for office %s", office_id)
        return _error(500, "Failed to change publication state.")


async def delete_office(office_id: int, db: AsyncSession):
    """Deletes the office; its children and translations cascade at the DB level.
    Stored images (director + staff) are swept from disk first."""
    try:
        office = await _load_by_id(db, office_id)
        if office is None:
            return _error(404, "Office not found.")

        images = [office.director_image_url] + [m.image_url for m in office.staff]
        await db.execute(sqlalchemy_delete(Office).where(Office.id == office_id))
        await db.commit()

        for path in images:
            if path and not path.startswith(("http://", "https://")):
                safe_delete_file(path)
        return JSONResponse(content={"status_code": 200, "message": "Office deleted."})
    except Exception:
        await db.rollback()
        logger.exception("Failed to delete office %s", office_id)
        return _error(500, "Failed to delete office.")


async def upload_image(office_id: int, file: UploadFile, db: AsyncSession):
    """Stores one image (director portrait or a staff photo) and returns its path.

    Like the About image upload, it only stores the file; the whole-office save
    drops the path into ``director_image_url`` or a staff row's ``image_url``.
    """
    try:
        office = (
            await db.execute(select(Office).where(Office.id == office_id))
        ).scalar_one_or_none()
        if office is None:
            return _error(404, "Office not found.")

        path = await save_upload(file, "offices", ALLOWED_IMAGE_MIMES)
        return JSONResponse(
            content={"status_code": 200, "message": "Image uploaded.", "path": path}
        )
    except HTTPException as exc:
        return _error(exc.status_code, str(exc.detail))
    except Exception:
        logger.exception("Failed to upload image for office %s", office_id)
        return _error(500, "Failed to upload image.")
