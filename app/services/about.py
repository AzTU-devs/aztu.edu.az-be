"""About-page CMS service.

Two read shapes, deliberately different:

* ``get_page_admin`` returns both languages side by side, plus inactive rows and
  every id, because the dashboard has to edit and reorder them.
* ``get_page_public`` resolves one language, drops anything inactive, and omits
  ids — it is what the website will consume once its pages are switched over.

Writes are narrow on purpose: a page's own fields, a section, an item, a person.
Nothing cascades a whole-page replace, so two editors working on different
sections of the same page cannot clobber each other.
"""

from datetime import datetime, timezone
from typing import Any, Iterable, Optional

from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete as sqlalchemy_delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.v1.schema.about import (
    CreateAboutItem,
    CreateAboutPage,
    CreateAboutPerson,
    CreateAboutSection,
    ReorderPayload,
    UpdateAboutItem,
    UpdateAboutPage,
    UpdateAboutPerson,
    UpdateAboutSection,
)
from app.core.logger import get_logger
from app.models.about.about_page import (
    AboutItem,
    AboutItemTr,
    AboutPage,
    AboutPageTr,
    AboutPerson,
    AboutPersonEducation,
    AboutPersonEducationTr,
    AboutPersonTr,
    AboutSection,
    AboutSectionTr,
)
from app.utils.file_upload import (
    ALLOWED_DOC_MIMES,
    ALLOWED_IMAGE_MIMES,
    safe_delete_file,
    save_upload,
)

logger = get_logger(__name__)

LANGS = ("az", "en")

PAGE_TR_FIELDS = (
    "eyebrow", "title", "subtitle", "breadcrumb", "intro", "meta_title", "meta_description",
)
PAGE_FIELDS = (
    "group_key", "template", "slug_az", "slug_en", "display_order",
    "hero_image", "hero_video_url", "cover_image", "pdf_url", "pdf_filename",
    "website_url", "video_url",
)

SECTION_FIELDS = (
    "section_key", "section_type", "display_order", "is_active",
    "image_url", "link_url", "pdf_url", "video_url", "icon", "extra",
)
SECTION_TR_FIELDS = (
    "title", "subtitle", "description", "body_html", "footer", "note",
    "cta_label", "pdf_url", "video_url", "list_intro", "headers",
)

ITEM_FIELDS = (
    "display_order", "item_key", "is_active", "image_url", "link_url", "pdf_url",
    "email", "phone", "icon", "slug", "year", "num", "value", "extra",
)
ITEM_TR_FIELDS = (
    "title", "subtitle", "description", "label", "value_text", "caption",
    "link_label", "file_url", "extra",
)

PERSON_FIELDS = (
    "display_order", "is_active", "slug", "image_url", "email", "phone",
    "phone_internal", "room_number",
)
PERSON_TR_FIELDS = (
    "full_name", "degree", "position", "office", "hours", "bio_html",
    "achievements", "research_interests",
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _error(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(content={"status_code": status_code, "message": message}, status_code=status_code)


def _apply(target: Any, data: dict, fields: Iterable[str]) -> None:
    """Copy only the keys the caller actually sent (PATCH semantics)."""
    for field in fields:
        if field in data:
            setattr(target, field, data[field])


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
                    getattr(model, fk_name) == fk_value,
                    model.lang_code == lang,
                )
            )
        ).scalar_one_or_none()

        if existing is None:
            existing = model(**{fk_name: fk_value}, lang_code=lang, created_at=now, updated_at=now)
            db.add(existing)

        _apply(existing, tr_data, fields)
        existing.updated_at = now


def _tr_map(translations: Iterable[Any], fields: Iterable[str]) -> dict:
    """`{az: {...}, en: {...}}`, with a blank record for a language never authored."""
    by_lang = {tr.lang_code: tr for tr in translations}
    out = {}
    for lang in LANGS:
        tr = by_lang.get(lang)
        out[lang] = {field: (getattr(tr, field) if tr else None) for field in fields}
    return out


def _is_blank(value: Any) -> bool:
    """Nothing an editor has actually filled in.

    Empty JSONB containers count: a table row whose EN cells were never typed
    arrives as ``[]``, not None, and rendering that verbatim would put a blank
    row on the English page instead of showing the Azerbaijani text.
    """
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def _pick(translations: Iterable[Any], lang: str, fields: Iterable[str]) -> dict:
    """One language's values, falling back to the other so a half-filled page still renders."""
    by_lang = {tr.lang_code: tr for tr in translations}
    primary = by_lang.get(lang)
    fallback = by_lang.get("az" if lang == "en" else "en")

    out = {}
    for field in fields:
        value = getattr(primary, field, None) if primary else None
        if _is_blank(value):
            value = getattr(fallback, field, None) if fallback else None
        out[field] = value
    return out


# ── Loading ────────────────────────────────────────────────────────────────────


def _page_query():
    return select(AboutPage).options(
        selectinload(AboutPage.translations),
        selectinload(AboutPage.sections).selectinload(AboutSection.translations),
        selectinload(AboutPage.sections)
        .selectinload(AboutSection.items)
        .selectinload(AboutItem.translations),
        selectinload(AboutPage.sections)
        .selectinload(AboutSection.people)
        .selectinload(AboutPerson.translations),
        selectinload(AboutPage.sections)
        .selectinload(AboutSection.people)
        .selectinload(AboutPerson.educations)
        .selectinload(AboutPersonEducation.translations),
    )


async def _load_page(db: AsyncSession, page_key: str) -> Optional[AboutPage]:
    result = await db.execute(_page_query().where(AboutPage.page_key == page_key))
    return result.scalars().unique().one_or_none()


def _serialize_person_admin(person: AboutPerson) -> dict:
    return {
        "id": person.id,
        **{field: getattr(person, field) for field in PERSON_FIELDS},
        **_tr_map(person.translations, PERSON_TR_FIELDS),
        "educations": [
            {
                "id": edu.id,
                "period": edu.period,
                "display_order": edu.display_order,
                **_tr_map(edu.translations, ("degree", "institution")),
            }
            for edu in sorted(person.educations, key=lambda e: e.display_order)
        ],
    }


def _serialize_section_admin(section: AboutSection) -> dict:
    return {
        "id": section.id,
        **{field: getattr(section, field) for field in SECTION_FIELDS},
        **_tr_map(section.translations, SECTION_TR_FIELDS),
        "items": [
            {
                "id": item.id,
                **{field: getattr(item, field) for field in ITEM_FIELDS},
                **_tr_map(item.translations, ITEM_TR_FIELDS),
            }
            for item in sorted(section.items, key=lambda i: i.display_order)
        ],
        "people": [
            _serialize_person_admin(person)
            for person in sorted(section.people, key=lambda p: p.display_order)
        ],
    }


def _serialize_page_admin(page: AboutPage) -> dict:
    return {
        "id": page.id,
        "page_key": page.page_key,
        "is_active": page.is_active,
        **{field: getattr(page, field) for field in PAGE_FIELDS},
        **_tr_map(page.translations, PAGE_TR_FIELDS),
        "sections": [
            _serialize_section_admin(section)
            for section in sorted(page.sections, key=lambda s: s.display_order)
        ],
        "created_at": page.created_at.isoformat() if page.created_at else None,
        "updated_at": page.updated_at.isoformat() if page.updated_at else None,
    }


def _serialize_page_public(page: AboutPage, lang: str) -> dict:
    sections = []
    for section in sorted(page.sections, key=lambda s: s.display_order):
        if not section.is_active:
            continue
        sections.append(
            {
                "section_key": section.section_key,
                "section_type": section.section_type,
                "image_url": section.image_url,
                "link_url": section.link_url,
                "pdf_url": section.pdf_url,
                "video_url": section.video_url,
                "icon": section.icon,
                "extra": section.extra,
                **_pick(section.translations, lang, SECTION_TR_FIELDS),
                "items": [
                    {
                        "item_key": item.item_key,
                        "image_url": item.image_url,
                        "link_url": item.link_url,
                        "pdf_url": item.pdf_url,
                        "email": item.email,
                        "phone": item.phone,
                        "icon": item.icon,
                        "slug": item.slug,
                        "year": item.year,
                        "num": item.num,
                        "value": item.value,
                        "extra": item.extra,
                        **_pick(item.translations, lang, ITEM_TR_FIELDS),
                    }
                    for item in sorted(section.items, key=lambda i: i.display_order)
                    if item.is_active
                ],
                "people": [
                    {
                        "slug": person.slug,
                        "image_url": person.image_url,
                        "email": person.email,
                        "phone": person.phone,
                        "phone_internal": person.phone_internal,
                        "room_number": person.room_number,
                        **_pick(person.translations, lang, PERSON_TR_FIELDS),
                        "educations": [
                            {
                                "period": edu.period,
                                **_pick(edu.translations, lang, ("degree", "institution")),
                            }
                            for edu in sorted(person.educations, key=lambda e: e.display_order)
                        ],
                    }
                    for person in sorted(section.people, key=lambda p: p.display_order)
                    if person.is_active
                ],
            }
        )

    return {
        "page_key": page.page_key,
        "group_key": page.group_key,
        "template": page.template,
        "slug": page.slug_az if lang == "az" else page.slug_en,
        "hero_image": page.hero_image,
        "hero_video_url": page.hero_video_url,
        "cover_image": page.cover_image,
        "pdf_url": page.pdf_url,
        "pdf_filename": page.pdf_filename,
        "website_url": page.website_url,
        "video_url": page.video_url,
        **_pick(page.translations, lang, PAGE_TR_FIELDS),
        "sections": sections,
    }


# ── Page reads ─────────────────────────────────────────────────────────────────


async def get_pages_admin(db: AsyncSession, lang: str = "az"):
    """Registry listing for the sidebar and the index screen — no section bodies."""
    try:
        result = await db.execute(
            select(AboutPage)
            .options(selectinload(AboutPage.translations))
            .order_by(AboutPage.display_order, AboutPage.id)
        )
        pages = result.scalars().unique().all()

        counts = dict(
            (
                await db.execute(
                    select(AboutSection.page_id, func.count(AboutSection.id)).group_by(
                        AboutSection.page_id
                    )
                )
            ).all()
        )

        payload = []
        for page in pages:
            titles = _tr_map(page.translations, ("title",))
            payload.append(
                {
                    "id": page.id,
                    "page_key": page.page_key,
                    "group_key": page.group_key,
                    "template": page.template,
                    "slug_az": page.slug_az,
                    "slug_en": page.slug_en,
                    "display_order": page.display_order,
                    "is_active": page.is_active,
                    "title_az": titles["az"]["title"],
                    "title_en": titles["en"]["title"],
                    "section_count": counts.get(page.id, 0),
                    "updated_at": page.updated_at.isoformat() if page.updated_at else None,
                }
            )

        return JSONResponse(content={"status_code": 200, "pages": payload, "total": len(payload)})
    except Exception:
        logger.exception("Failed to list about pages")
        return _error(500, "Failed to list about pages.")


async def get_page_admin(page_key: str, db: AsyncSession):
    try:
        page = await _load_page(db, page_key)
        if page is None:
            return _error(404, "About page not found.")
        return JSONResponse(content={"status_code": 200, "page": _serialize_page_admin(page)})
    except Exception:
        logger.exception("Failed to load about page %s", page_key)
        return _error(500, "Failed to load about page.")


async def get_page_public(page_key: str, lang: str, db: AsyncSession):
    try:
        page = await _load_page(db, page_key)
        if page is None or not page.is_active:
            return _error(404, "About page not found.")
        return JSONResponse(content={"status_code": 200, "page": _serialize_page_public(page, lang)})
    except Exception:
        logger.exception("Failed to load public about page %s", page_key)
        return _error(500, "Failed to load about page.")


async def get_pages_public(lang: str, db: AsyncSession):
    """The published navigation tree — what the header dropdown would render."""
    try:
        result = await db.execute(
            select(AboutPage)
            .options(selectinload(AboutPage.translations))
            .where(AboutPage.is_active.is_(True))
            .order_by(AboutPage.display_order, AboutPage.id)
        )
        pages = result.scalars().unique().all()

        payload = [
            {
                "page_key": page.page_key,
                "group_key": page.group_key,
                "template": page.template,
                "slug": page.slug_az if lang == "az" else page.slug_en,
                **_pick(page.translations, lang, ("title", "breadcrumb")),
            }
            for page in pages
        ]
        return JSONResponse(content={"status_code": 200, "pages": payload, "total": len(payload)})
    except Exception:
        logger.exception("Failed to list public about pages")
        return _error(500, "Failed to list about pages.")


# ── Page writes ────────────────────────────────────────────────────────────────


async def create_page(request: CreateAboutPage, db: AsyncSession):
    try:
        existing = (
            await db.execute(select(AboutPage.id).where(AboutPage.page_key == request.page_key))
        ).scalar_one_or_none()
        if existing:
            return _error(409, "A page with this key already exists.")

        now = _now()
        data = request.dict(exclude_unset=True)

        page = AboutPage(page_key=request.page_key, created_at=now, updated_at=now)
        _apply(page, data, PAGE_FIELDS)
        db.add(page)
        await db.flush()

        await _upsert_translations(db, AboutPageTr, "page_id", page.id, data, PAGE_TR_FIELDS, now)
        await db.commit()

        return JSONResponse(
            content={"status_code": 201, "message": "About page created.", "page_key": page.page_key},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception:
        await db.rollback()
        logger.exception("Failed to create about page")
        return _error(500, "Failed to create about page.")


async def update_page(page_key: str, request: UpdateAboutPage, db: AsyncSession):
    try:
        page = (
            await db.execute(select(AboutPage).where(AboutPage.page_key == page_key))
        ).scalar_one_or_none()
        if page is None:
            return _error(404, "About page not found.")

        now = _now()
        data = request.dict(exclude_unset=True)

        _apply(page, data, PAGE_FIELDS)
        page.updated_at = now

        await _upsert_translations(db, AboutPageTr, "page_id", page.id, data, PAGE_TR_FIELDS, now)
        await db.commit()

        return JSONResponse(content={"status_code": 200, "message": "About page updated."})
    except Exception:
        await db.rollback()
        logger.exception("Failed to update about page %s", page_key)
        return _error(500, "Failed to update about page.")


async def publish_page(page_key: str, is_active: bool, db: AsyncSession):
    """The only way a page goes live. Kept off `update_page` so that saving a
    half-written paragraph can never publish the screen by accident."""
    try:
        page = (
            await db.execute(select(AboutPage).where(AboutPage.page_key == page_key))
        ).scalar_one_or_none()
        if page is None:
            return _error(404, "About page not found.")

        page.is_active = is_active
        page.updated_at = _now()
        await db.commit()

        return JSONResponse(
            content={
                "status_code": 200,
                "message": "About page published." if is_active else "About page unpublished.",
                "is_active": is_active,
            }
        )
    except Exception:
        await db.rollback()
        logger.exception("Failed to publish about page %s", page_key)
        return _error(500, "Failed to change publication state.")


async def delete_page(page_key: str, db: AsyncSession):
    try:
        page = (
            await db.execute(select(AboutPage).where(AboutPage.page_key == page_key))
        ).scalar_one_or_none()
        if page is None:
            return _error(404, "About page not found.")

        await db.execute(sqlalchemy_delete(AboutPage).where(AboutPage.id == page.id))
        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "About page deleted."})
    except Exception:
        await db.rollback()
        logger.exception("Failed to delete about page %s", page_key)
        return _error(500, "Failed to delete about page.")


# ── Sections ───────────────────────────────────────────────────────────────────


async def create_section(page_key: str, request: CreateAboutSection, db: AsyncSession):
    try:
        page = (
            await db.execute(select(AboutPage).where(AboutPage.page_key == page_key))
        ).scalar_one_or_none()
        if page is None:
            return _error(404, "About page not found.")

        clash = (
            await db.execute(
                select(AboutSection.id).where(
                    AboutSection.page_id == page.id,
                    AboutSection.section_key == request.section_key,
                )
            )
        ).scalar_one_or_none()
        if clash:
            return _error(409, "A section with this key already exists on the page.")

        now = _now()
        data = request.dict(exclude_unset=True)

        if "display_order" not in data:
            highest = (
                await db.execute(
                    select(func.max(AboutSection.display_order)).where(AboutSection.page_id == page.id)
                )
            ).scalar_one_or_none()
            data["display_order"] = (highest or 0) + 1

        section = AboutSection(page_id=page.id, created_at=now, updated_at=now)
        _apply(section, data, SECTION_FIELDS)
        db.add(section)
        await db.flush()

        await _upsert_translations(
            db, AboutSectionTr, "section_id", section.id, data, SECTION_TR_FIELDS, now
        )
        await db.commit()

        return JSONResponse(
            content={"status_code": 201, "message": "Section created.", "id": section.id},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception:
        await db.rollback()
        logger.exception("Failed to create section on %s", page_key)
        return _error(500, "Failed to create section.")


async def update_section(section_id: int, request: UpdateAboutSection, db: AsyncSession):
    try:
        section = (
            await db.execute(select(AboutSection).where(AboutSection.id == section_id))
        ).scalar_one_or_none()
        if section is None:
            return _error(404, "Section not found.")

        now = _now()
        data = request.dict(exclude_unset=True)

        _apply(section, data, SECTION_FIELDS)
        section.updated_at = now

        await _upsert_translations(
            db, AboutSectionTr, "section_id", section.id, data, SECTION_TR_FIELDS, now
        )
        await db.commit()

        return JSONResponse(content={"status_code": 200, "message": "Section updated."})
    except Exception:
        await db.rollback()
        logger.exception("Failed to update section %s", section_id)
        return _error(500, "Failed to update section.")


async def delete_section(section_id: int, db: AsyncSession):
    try:
        section = (
            await db.execute(select(AboutSection).where(AboutSection.id == section_id))
        ).scalar_one_or_none()
        if section is None:
            return _error(404, "Section not found.")

        await db.execute(sqlalchemy_delete(AboutSection).where(AboutSection.id == section_id))
        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "Section deleted."})
    except Exception:
        await db.rollback()
        logger.exception("Failed to delete section %s", section_id)
        return _error(500, "Failed to delete section.")


# ── Items ──────────────────────────────────────────────────────────────────────


async def create_item(section_id: int, request: CreateAboutItem, db: AsyncSession):
    try:
        section = (
            await db.execute(select(AboutSection.id).where(AboutSection.id == section_id))
        ).scalar_one_or_none()
        if section is None:
            return _error(404, "Section not found.")

        now = _now()
        data = request.dict(exclude_unset=True)

        if "display_order" not in data:
            highest = (
                await db.execute(
                    select(func.max(AboutItem.display_order)).where(AboutItem.section_id == section_id)
                )
            ).scalar_one_or_none()
            data["display_order"] = (highest or 0) + 1

        item = AboutItem(section_id=section_id, created_at=now, updated_at=now)
        _apply(item, data, ITEM_FIELDS)
        db.add(item)
        await db.flush()

        await _upsert_translations(db, AboutItemTr, "item_id", item.id, data, ITEM_TR_FIELDS, now)
        await db.commit()

        return JSONResponse(
            content={"status_code": 201, "message": "Item created.", "id": item.id},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception:
        await db.rollback()
        logger.exception("Failed to create item in section %s", section_id)
        return _error(500, "Failed to create item.")


async def update_item(item_id: int, request: UpdateAboutItem, db: AsyncSession):
    try:
        item = (
            await db.execute(select(AboutItem).where(AboutItem.id == item_id))
        ).scalar_one_or_none()
        if item is None:
            return _error(404, "Item not found.")

        now = _now()
        data = request.dict(exclude_unset=True)

        _apply(item, data, ITEM_FIELDS)
        item.updated_at = now

        await _upsert_translations(db, AboutItemTr, "item_id", item.id, data, ITEM_TR_FIELDS, now)
        await db.commit()

        return JSONResponse(content={"status_code": 200, "message": "Item updated."})
    except Exception:
        await db.rollback()
        logger.exception("Failed to update item %s", item_id)
        return _error(500, "Failed to update item.")


async def delete_item(item_id: int, db: AsyncSession):
    try:
        item = (
            await db.execute(select(AboutItem).where(AboutItem.id == item_id))
        ).scalar_one_or_none()
        if item is None:
            return _error(404, "Item not found.")

        if item.image_url:
            safe_delete_file(item.image_url)

        await db.execute(sqlalchemy_delete(AboutItem).where(AboutItem.id == item_id))
        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "Item deleted."})
    except Exception:
        await db.rollback()
        logger.exception("Failed to delete item %s", item_id)
        return _error(500, "Failed to delete item.")


# ── People ─────────────────────────────────────────────────────────────────────


async def _replace_educations(db: AsyncSession, person_id: int, educations: list, now: datetime):
    await db.execute(
        sqlalchemy_delete(AboutPersonEducation).where(AboutPersonEducation.person_id == person_id)
    )
    for index, entry in enumerate(educations):
        payload = entry if isinstance(entry, dict) else entry.dict(exclude_unset=True)
        education = AboutPersonEducation(
            person_id=person_id,
            period=payload.get("period"),
            display_order=payload.get("display_order", index),
            created_at=now,
            updated_at=now,
        )
        db.add(education)
        await db.flush()
        await _upsert_translations(
            db,
            AboutPersonEducationTr,
            "education_id",
            education.id,
            payload,
            ("degree", "institution"),
            now,
        )


async def create_person(section_id: int, request: CreateAboutPerson, db: AsyncSession):
    try:
        section = (
            await db.execute(select(AboutSection.id).where(AboutSection.id == section_id))
        ).scalar_one_or_none()
        if section is None:
            return _error(404, "Section not found.")

        now = _now()
        data = request.dict(exclude_unset=True)

        if "display_order" not in data:
            highest = (
                await db.execute(
                    select(func.max(AboutPerson.display_order)).where(
                        AboutPerson.section_id == section_id
                    )
                )
            ).scalar_one_or_none()
            data["display_order"] = (highest or 0) + 1

        person = AboutPerson(section_id=section_id, created_at=now, updated_at=now)
        _apply(person, data, PERSON_FIELDS)
        db.add(person)
        await db.flush()

        await _upsert_translations(db, AboutPersonTr, "person_id", person.id, data, PERSON_TR_FIELDS, now)
        if data.get("educations") is not None:
            await _replace_educations(db, person.id, data["educations"], now)

        await db.commit()
        return JSONResponse(
            content={"status_code": 201, "message": "Person created.", "id": person.id},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception:
        await db.rollback()
        logger.exception("Failed to create person in section %s", section_id)
        return _error(500, "Failed to create person.")


async def update_person(person_id: int, request: UpdateAboutPerson, db: AsyncSession):
    try:
        person = (
            await db.execute(select(AboutPerson).where(AboutPerson.id == person_id))
        ).scalar_one_or_none()
        if person is None:
            return _error(404, "Person not found.")

        now = _now()
        data = request.dict(exclude_unset=True)

        _apply(person, data, PERSON_FIELDS)
        person.updated_at = now

        await _upsert_translations(db, AboutPersonTr, "person_id", person.id, data, PERSON_TR_FIELDS, now)
        # Absent key means "leave educations alone"; an explicit [] clears them.
        if data.get("educations") is not None:
            await _replace_educations(db, person.id, data["educations"], now)

        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "Person updated."})
    except Exception:
        await db.rollback()
        logger.exception("Failed to update person %s", person_id)
        return _error(500, "Failed to update person.")


async def delete_person(person_id: int, db: AsyncSession):
    try:
        person = (
            await db.execute(select(AboutPerson).where(AboutPerson.id == person_id))
        ).scalar_one_or_none()
        if person is None:
            return _error(404, "Person not found.")

        if person.image_url:
            safe_delete_file(person.image_url)

        await db.execute(sqlalchemy_delete(AboutPerson).where(AboutPerson.id == person_id))
        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "Person deleted."})
    except Exception:
        await db.rollback()
        logger.exception("Failed to delete person %s", person_id)
        return _error(500, "Failed to delete person.")


# ── Reordering ─────────────────────────────────────────────────────────────────


async def _reorder(db: AsyncSession, model: Any, parent_attr: str, parent_id: int, ids: list[int]):
    rows = (
        await db.execute(select(model).where(getattr(model, parent_attr) == parent_id))
    ).scalars().all()
    by_id = {row.id: row for row in rows}

    unknown = [row_id for row_id in ids if row_id not in by_id]
    if unknown:
        return _error(400, f"Ids not in this parent: {unknown}")

    now = _now()
    for position, row_id in enumerate(ids):
        by_id[row_id].display_order = position
        by_id[row_id].updated_at = now

    await db.commit()
    return JSONResponse(content={"status_code": 200, "message": "Order updated."})


async def reorder_sections(page_key: str, payload: ReorderPayload, db: AsyncSession):
    try:
        page = (
            await db.execute(select(AboutPage).where(AboutPage.page_key == page_key))
        ).scalar_one_or_none()
        if page is None:
            return _error(404, "About page not found.")
        return await _reorder(db, AboutSection, "page_id", page.id, payload.ids)
    except Exception:
        await db.rollback()
        logger.exception("Failed to reorder sections on %s", page_key)
        return _error(500, "Failed to reorder sections.")


async def reorder_items(section_id: int, payload: ReorderPayload, db: AsyncSession):
    try:
        return await _reorder(db, AboutItem, "section_id", section_id, payload.ids)
    except Exception:
        await db.rollback()
        logger.exception("Failed to reorder items in %s", section_id)
        return _error(500, "Failed to reorder items.")


async def reorder_people(section_id: int, payload: ReorderPayload, db: AsyncSession):
    try:
        return await _reorder(db, AboutPerson, "section_id", section_id, payload.ids)
    except Exception:
        await db.rollback()
        logger.exception("Failed to reorder people in %s", section_id)
        return _error(500, "Failed to reorder people.")


# ── Uploads ────────────────────────────────────────────────────────────────────


async def _store(upload: UploadFile, subdirectory: str, mimes: dict) -> str:
    return await save_upload(upload, subdirectory, mimes)


async def upload_page_image(page_key: str, field: str, image: UploadFile, db: AsyncSession):
    if field not in ("hero_image", "cover_image"):
        return _error(400, "field must be hero_image or cover_image.")
    try:
        page = (
            await db.execute(select(AboutPage).where(AboutPage.page_key == page_key))
        ).scalar_one_or_none()
        if page is None:
            return _error(404, "About page not found.")

        previous = getattr(page, field)
        path = await _store(image, "about", ALLOWED_IMAGE_MIMES)
        setattr(page, field, path)
        page.updated_at = _now()
        await db.commit()

        if previous:
            safe_delete_file(previous)
        return JSONResponse(content={"status_code": 200, "message": "Image uploaded.", "path": path})
    except Exception:
        await db.rollback()
        logger.exception("Failed to upload %s for %s", field, page_key)
        return _error(500, "Failed to upload image.")


async def upload_page_file(page_key: str, file: UploadFile, db: AsyncSession):
    try:
        page = (
            await db.execute(select(AboutPage).where(AboutPage.page_key == page_key))
        ).scalar_one_or_none()
        if page is None:
            return _error(404, "About page not found.")

        previous = page.pdf_url
        path = await _store(file, "about/documents", ALLOWED_DOC_MIMES)
        page.pdf_url = path
        page.pdf_filename = file.filename
        page.updated_at = _now()
        await db.commit()

        if previous:
            safe_delete_file(previous)
        return JSONResponse(content={"status_code": 200, "message": "File uploaded.", "path": path})
    except Exception:
        await db.rollback()
        logger.exception("Failed to upload file for %s", page_key)
        return _error(500, "Failed to upload file.")


async def upload_item_image(item_id: int, image: UploadFile, db: AsyncSession):
    try:
        item = (
            await db.execute(select(AboutItem).where(AboutItem.id == item_id))
        ).scalar_one_or_none()
        if item is None:
            return _error(404, "Item not found.")

        previous = item.image_url
        path = await _store(image, "about", ALLOWED_IMAGE_MIMES)
        item.image_url = path
        item.updated_at = _now()
        await db.commit()

        if previous:
            safe_delete_file(previous)
        return JSONResponse(content={"status_code": 200, "message": "Image uploaded.", "path": path})
    except Exception:
        await db.rollback()
        logger.exception("Failed to upload image for item %s", item_id)
        return _error(500, "Failed to upload image.")


async def upload_item_file(item_id: int, lang: Optional[str], file: UploadFile, db: AsyncSession):
    """Language-neutral file goes on the item; an AZ/EN pair goes on its translation."""
    try:
        item = (
            await db.execute(select(AboutItem).where(AboutItem.id == item_id))
        ).scalar_one_or_none()
        if item is None:
            return _error(404, "Item not found.")

        now = _now()
        path = await _store(file, "about/documents", ALLOWED_DOC_MIMES)

        if lang in LANGS:
            tr = (
                await db.execute(
                    select(AboutItemTr).where(
                        AboutItemTr.item_id == item_id, AboutItemTr.lang_code == lang
                    )
                )
            ).scalar_one_or_none()
            if tr is None:
                tr = AboutItemTr(item_id=item_id, lang_code=lang, created_at=now, updated_at=now)
                db.add(tr)
            previous = tr.file_url
            tr.file_url = path
            tr.updated_at = now
        else:
            previous = item.pdf_url
            item.pdf_url = path

        item.updated_at = now
        await db.commit()

        if previous:
            safe_delete_file(previous)
        return JSONResponse(content={"status_code": 200, "message": "File uploaded.", "path": path})
    except Exception:
        await db.rollback()
        logger.exception("Failed to upload file for item %s", item_id)
        return _error(500, "Failed to upload file.")


async def upload_person_image(person_id: int, image: UploadFile, db: AsyncSession):
    try:
        person = (
            await db.execute(select(AboutPerson).where(AboutPerson.id == person_id))
        ).scalar_one_or_none()
        if person is None:
            return _error(404, "Person not found.")

        previous = person.image_url
        path = await _store(image, "about/people", ALLOWED_IMAGE_MIMES)
        person.image_url = path
        person.updated_at = _now()
        await db.commit()

        if previous:
            safe_delete_file(previous)
        return JSONResponse(content={"status_code": 200, "message": "Image uploaded.", "path": path})
    except Exception:
        await db.rollback()
        logger.exception("Failed to upload image for person %s", person_id)
        return _error(500, "Failed to upload image.")
