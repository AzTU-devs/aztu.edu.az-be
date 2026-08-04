"""About-section service.

Two read shapes, deliberately different:

* ``get_page_admin`` returns both languages side by side plus every id, because
  the dashboard edits them together.
* ``get_page_public`` resolves one language, refuses unpublished pages, and adds
  the derived SEO fields — it is what the website consumes.

The page saves as one document. `blocks` and `links` arrive whole and replace
what is stored, which matches the dashboard's single Save button and avoids a
per-row endpoint surface for a page this small.
"""

import re
from datetime import datetime, timezone
from typing import Any, Iterable, Optional

from fastapi import HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete as sqlalchemy_delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.v1.schema.about import UpdateAboutPage
from app.core.logger import get_logger
from app.models.about.about import (
    AboutBlock,
    AboutBlockTr,
    AboutCouncil,
    AboutCouncilMember,
    AboutCouncilMemberTr,
    AboutCouncilTr,
    AboutDocCategory,
    AboutDocCategoryTr,
    AboutDocument,
    AboutDocumentTr,
    AboutImage,
    AboutLink,
    AboutLinkTr,
    AboutList,
    AboutListTr,
    AboutPerson,
    AboutPersonTr,
    AboutPillar,
    AboutPillarTr,
    AboutMilestone,
    AboutMilestoneTr,
    AboutPage,
    AboutPageTr,
)
from app.utils.file_upload import (
    ALLOWED_DOC_MIMES,
    ALLOWED_IMAGE_MIMES,
    safe_delete_file,
    save_upload,
)
from app.utils.html_sanitizer import sanitize_html

logger = get_logger(__name__)

LANGS = ("az", "en")

PAGE_TR_FIELDS = (
    "title", "description", "links_title", "document_label", "pillars_title",
    # Rector page.
    "degree", "position", "message", "about",
    # Vice-rector page.
    "domains", "section_title", "section_body",
    # Scientific-board page.
    "councils_title",
)
BLOCK_TR_FIELDS = ("title", "body")
LINK_TR_FIELDS = ("label",)
MILESTONE_TR_FIELDS = ("title", "description")
PILLAR_TR_FIELDS = ("title", "description", "tags")
LIST_TR_FIELDS = ("title", "items")
PERSON_FIELDS = ("email", "phone", "phone_code", "image_url", "year_start", "year_end")
PERSON_TR_FIELDS = ("name", "surname", "degree", "position", "bio")
COUNCIL_TR_FIELDS = ("name",)
COUNCIL_MEMBER_TR_FIELDS = ("name", "surname", "position")
DOC_CATEGORY_TR_FIELDS = ("name",)
DOCUMENT_TR_FIELDS = ("name", "file_url")

# Language-neutral page columns writable from the dashboard (rector page).
PAGE_FIELDS = ("slug_az", "slug_en", "document_url", "experience", "email", "image_url")

# Editor-authored HTML. Scrubbed on the way in so the website can render it
# verbatim — an authenticated admin is still not a reason to store raw markup.
# `message` and `about` are the rector page's rich-text fields.
RICH_TEXT_FIELDS = frozenset({"description", "body", "message", "about", "section_body", "bio"})

# SEO is derived here rather than typed in the dashboard: the meta description
# is the hero copy with its markup removed, clipped to a sensible length.
SEO_DESCRIPTION_LIMIT = 160


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _error(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(
        content={"status_code": status_code, "message": message}, status_code=status_code
    )


def _milestone_order(milestone: Any) -> tuple:
    """Newest first, as the page requires.

    The year is free text, so the sort reads the first 3-4 digit run out of it
    ("1887-1905" sorts as 1887). An entry with no digits is the present day
    ("Bu gün" / "Today") and therefore sorts ahead of every dated one.
    `display_order` only breaks ties.
    """
    match = re.search(r"\d{3,4}", milestone.year or "")
    if match is None:
        return (0, 0, milestone.display_order)
    return (1, -int(match.group()), milestone.display_order)


def _milestone_sort(page: AboutPage):
    """The timeline sorts newest-first by year; every other page (the academic
    calendar's semesters) keeps the order the editor arranged."""
    return _milestone_order if page.template == "timeline" else (lambda m: m.display_order)


def _grade_scale_public(page: AboutPage, lang: str) -> list:
    """The grade-scale rows with each description resolved to one language."""
    rows = page.grade_scale or []
    out = []
    for row in rows:
        description = row.get(f"description_{lang}") or row.get("description_az") or row.get("description_en")
        out.append({"points": row.get("points"), "grade": row.get("grade"), "description": description})
    return out


def _plain_text(html: Optional[str]) -> str:
    """Markup stripped and whitespace collapsed — for meta tags."""
    if not html:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def _seo_description(html: Optional[str]) -> str:
    text = _plain_text(html)
    if len(text) <= SEO_DESCRIPTION_LIMIT:
        return text
    # Cut on a word boundary so the tag never ends mid-word.
    return text[:SEO_DESCRIPTION_LIMIT].rsplit(" ", 1)[0] + "…"


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
    """One language's values, falling back to the other so a half-filled page still renders."""
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


ROLE_MEMBER = "member"
ROLE_SECRETARY = "secretary"


def _members(council: Any, role: str) -> list:
    """One council's roster for a role, in display order."""
    return sorted(
        (m for m in council.members if m.role == role),
        key=lambda m: m.display_order,
    )


def _members_admin(council: Any, role: str) -> list:
    return [
        {
            "id": member.id,
            "display_order": member.display_order,
            **_tr_map(member.translations, COUNCIL_MEMBER_TR_FIELDS),
        }
        for member in _members(council, role)
    ]


def _members_public(council: Any, role: str, lang: str) -> list:
    return [
        _pick(member.translations, lang, COUNCIL_MEMBER_TR_FIELDS)
        for member in _members(council, role)
    ]


# ── Loading ────────────────────────────────────────────────────────────────────


def _page_query():
    return select(AboutPage).options(
        selectinload(AboutPage.translations),
        selectinload(AboutPage.blocks).selectinload(AboutBlock.translations),
        selectinload(AboutPage.links).selectinload(AboutLink.translations),
        selectinload(AboutPage.milestones).selectinload(AboutMilestone.translations),
        selectinload(AboutPage.pillars).selectinload(AboutPillar.translations),
        selectinload(AboutPage.lists).selectinload(AboutList.translations),
        selectinload(AboutPage.images),
        selectinload(AboutPage.persons).selectinload(AboutPerson.translations),
        selectinload(AboutPage.councils).selectinload(AboutCouncil.translations),
        selectinload(AboutPage.councils)
        .selectinload(AboutCouncil.members)
        .selectinload(AboutCouncilMember.translations),
        selectinload(AboutPage.doc_categories).selectinload(AboutDocCategory.translations),
        selectinload(AboutPage.documents).selectinload(AboutDocument.translations),
    )


async def _load_page(db: AsyncSession, page_key: str) -> Optional[AboutPage]:
    result = await db.execute(_page_query().where(AboutPage.page_key == page_key))
    return result.scalars().unique().one_or_none()


def _serialize_admin(page: AboutPage) -> dict:
    return {
        "id": page.id,
        "page_key": page.page_key,
        "template": page.template,
        "slug_az": page.slug_az,
        "slug_en": page.slug_en,
        "document_url": page.document_url,
        "experience": page.experience,
        "email": page.email,
        "image_url": page.image_url,
        "grade_scale": page.grade_scale or [],
        "is_active": page.is_active,
        **_tr_map(page.translations, PAGE_TR_FIELDS),
        "blocks": [
            {
                "id": block.id,
                "block_key": block.block_key,
                "display_order": block.display_order,
                **_tr_map(block.translations, BLOCK_TR_FIELDS),
            }
            for block in sorted(page.blocks, key=lambda b: b.display_order)
        ],
        "links": [
            {
                "id": link.id,
                "url": link.url,
                "display_order": link.display_order,
                **_tr_map(link.translations, LINK_TR_FIELDS),
            }
            for link in sorted(page.links, key=lambda l: l.display_order)
        ],
        "milestones": [
            {
                "id": milestone.id,
                "year": milestone.year,
                **_tr_map(milestone.translations, MILESTONE_TR_FIELDS),
            }
            for milestone in sorted(page.milestones, key=_milestone_sort(page))
        ],
        "pillars": [
            {
                "id": pillar.id,
                "display_order": pillar.display_order,
                **_tr_map(pillar.translations, PILLAR_TR_FIELDS),
            }
            for pillar in sorted(page.pillars, key=lambda r: r.display_order)
        ],
        "lists": [
            {
                "id": entry.id,
                "list_key": entry.list_key,
                "style": entry.style,
                **_tr_map(entry.translations, LIST_TR_FIELDS),
            }
            for entry in sorted(page.lists, key=lambda l: l.display_order)
        ],
        "images": [
            {
                "id": image.id,
                "image_url": image.image_url,
                "display_order": image.display_order,
            }
            for image in sorted(page.images, key=lambda i: i.display_order)
        ],
        "persons": [
            {
                "id": person.id,
                "display_order": person.display_order,
                **{field: getattr(person, field) for field in PERSON_FIELDS},
                **_tr_map(person.translations, PERSON_TR_FIELDS),
            }
            for person in sorted(page.persons, key=lambda x: x.display_order)
        ],
        "councils": [
            {
                "id": council.id,
                "display_order": council.display_order,
                **_tr_map(council.translations, COUNCIL_TR_FIELDS),
                "members": _members_admin(council, ROLE_MEMBER),
                "secretaries": _members_admin(council, ROLE_SECRETARY),
            }
            for council in sorted(page.councils, key=lambda c: c.display_order)
        ],
        "doc_categories": [
            {
                "id": category.id,
                "category_key": category.category_key,
                "display_order": category.display_order,
                **_tr_map(category.translations, DOC_CATEGORY_TR_FIELDS),
            }
            for category in sorted(page.doc_categories, key=lambda c: c.display_order)
        ],
        "documents": [
            {
                "id": document.id,
                "category_key": document.category_key,
                "display_order": document.display_order,
                **_tr_map(document.translations, DOCUMENT_TR_FIELDS),
            }
            for document in sorted(page.documents, key=lambda d: d.display_order)
        ],
        "updated_at": page.updated_at.isoformat() if page.updated_at else None,
    }


def _serialize_public(page: AboutPage, lang: str) -> dict:
    copy = _pick(page.translations, lang, PAGE_TR_FIELDS)
    return {
        "page_key": page.page_key,
        "template": page.template,
        "slug": page.slug_az if lang == "az" else page.slug_en,
        "document_url": page.document_url,
        "experience": page.experience,
        "email": page.email,
        "image_url": page.image_url,
        "grade_scale": _grade_scale_public(page, lang),
        **copy,
        # Derived, not authored: the dashboard has no SEO fields by design.
        "seo": {
            "title": copy.get("title"),
            "description": _seo_description(copy.get("description")),
        },
        "blocks": [
            {
                "block_key": block.block_key,
                **_pick(block.translations, lang, BLOCK_TR_FIELDS),
            }
            for block in sorted(page.blocks, key=lambda b: b.display_order)
        ],
        "links": [
            {
                "url": link.url,
                **_pick(link.translations, lang, LINK_TR_FIELDS),
            }
            for link in sorted(page.links, key=lambda l: l.display_order)
        ],
        "milestones": [
            {
                "year": milestone.year,
                **_pick(milestone.translations, lang, MILESTONE_TR_FIELDS),
            }
            for milestone in sorted(page.milestones, key=_milestone_sort(page))
        ],
        "pillars": [
            _pick(pillar.translations, lang, PILLAR_TR_FIELDS)
            for pillar in sorted(page.pillars, key=lambda r: r.display_order)
        ],
        "lists": [
            {
                "list_key": entry.list_key,
                "style": entry.style,
                **_pick(entry.translations, lang, LIST_TR_FIELDS),
            }
            for entry in sorted(page.lists, key=lambda l: l.display_order)
        ],
        "images": [
            image.image_url
            for image in sorted(page.images, key=lambda i: i.display_order)
        ],
        "persons": [
            {
                **{field: getattr(person, field) for field in PERSON_FIELDS},
                **_pick(person.translations, lang, PERSON_TR_FIELDS),
            }
            for person in sorted(page.persons, key=lambda x: x.display_order)
        ],
        "councils": [
            {
                **_pick(council.translations, lang, COUNCIL_TR_FIELDS),
                "members": _members_public(council, ROLE_MEMBER, lang),
                "secretaries": _members_public(council, ROLE_SECRETARY, lang),
            }
            for council in sorted(page.councils, key=lambda c: c.display_order)
        ],
        "doc_categories": [
            {
                "category_key": category.category_key,
                **_pick(category.translations, lang, DOC_CATEGORY_TR_FIELDS),
            }
            for category in sorted(page.doc_categories, key=lambda c: c.display_order)
        ],
        "documents": [
            {
                "category_key": document.category_key,
                **_pick(document.translations, lang, DOCUMENT_TR_FIELDS),
            }
            for document in sorted(page.documents, key=lambda d: d.display_order)
        ],
    }


# ── Reads ──────────────────────────────────────────────────────────────────────


async def get_pages_admin(db: AsyncSession):
    """Registry listing — what the sidebar and any future index screen show."""
    try:
        result = await db.execute(
            _page_query().order_by(AboutPage.display_order, AboutPage.id)
        )
        pages = result.scalars().unique().all()
        payload = [
            {
                "page_key": page.page_key,
                "template": page.template,
                "is_active": page.is_active,
                "title_az": _tr_map(page.translations, ("title",))["az"]["title"],
                "title_en": _tr_map(page.translations, ("title",))["en"]["title"],
                "updated_at": page.updated_at.isoformat() if page.updated_at else None,
            }
            for page in pages
        ]
        return JSONResponse(content={"status_code": 200, "pages": payload})
    except Exception:
        logger.exception("Failed to list about pages")
        return _error(500, "Failed to list about pages.")


async def get_page_admin(page_key: str, db: AsyncSession):
    try:
        page = await _load_page(db, page_key)
        if page is None:
            return _error(404, "About page not found.")
        return JSONResponse(content={"status_code": 200, "page": _serialize_admin(page)})
    except Exception:
        logger.exception("Failed to load about page %s", page_key)
        return _error(500, "Failed to load about page.")


async def get_page_public(page_key: str, lang: str, db: AsyncSession):
    try:
        page = await _load_page(db, page_key)
        if page is None or not page.is_active:
            return _error(404, "About page not found.")
        return JSONResponse(
            content={"status_code": 200, "page": _serialize_public(page, lang)}
        )
    except Exception:
        logger.exception("Failed to load public about page %s", page_key)
        return _error(500, "Failed to load about page.")


# ── Writes ─────────────────────────────────────────────────────────────────────


async def _replace_blocks(db: AsyncSession, page_id: int, blocks: list, now: datetime):
    """Rewrites the card list in the order given.

    Rows are matched by ``block_key`` rather than deleted and recreated, so an
    id stays stable across saves and the website can keep addressing a card by
    its key. Keys absent from the payload are removed.
    """
    existing = {
        block.block_key: block
        for block in (
            await db.execute(select(AboutBlock).where(AboutBlock.page_id == page_id))
        ).scalars().all()
    }

    seen: set[str] = set()
    for index, entry in enumerate(blocks):
        payload = entry if isinstance(entry, dict) else entry.dict(exclude_unset=True)
        key = (payload.get("block_key") or "").strip()
        if not key:
            continue
        seen.add(key)

        block = existing.get(key)
        if block is None:
            block = AboutBlock(
                page_id=page_id, block_key=key, created_at=now, updated_at=now
            )
            db.add(block)
            await db.flush()

        block.display_order = index
        block.updated_at = now
        await _upsert_translations(
            db, AboutBlockTr, "block_id", block.id, payload, BLOCK_TR_FIELDS, now
        )

    stale = [block.id for key, block in existing.items() if key not in seen]
    if stale:
        await db.execute(sqlalchemy_delete(AboutBlock).where(AboutBlock.id.in_(stale)))


async def _replace_links(db: AsyncSession, page_id: int, links: list, now: datetime):
    """Rewrites the button list. Buttons carry no stable key, so they are
    replaced wholesale — the payload is the complete, ordered truth."""
    await db.execute(sqlalchemy_delete(AboutLink).where(AboutLink.page_id == page_id))

    for index, entry in enumerate(links):
        payload = entry if isinstance(entry, dict) else entry.dict(exclude_unset=True)
        link = AboutLink(
            page_id=page_id,
            url=payload.get("url"),
            display_order=index,
            created_at=now,
            updated_at=now,
        )
        db.add(link)
        await db.flush()
        await _upsert_translations(
            db, AboutLinkTr, "link_id", link.id, payload, LINK_TR_FIELDS, now
        )


async def _replace_images(db: AsyncSession, page_id: int, images: list, now: datetime):
    """Rewrites the gallery in the order given.

    Images carry no stable key, so the payload is the complete, ordered truth.
    Any stored file that was dropped from the strip is removed from disk so the
    static directory does not fill up with orphans; a pasted URL is left alone.
    """
    kept: set[str] = set()
    rows = []
    for index, entry in enumerate(images):
        payload = entry if isinstance(entry, dict) else entry.dict(exclude_unset=True)
        url = (payload.get("image_url") or "").strip()
        if not url:
            continue
        kept.add(url)
        rows.append((index, url))

    previous = (
        await db.execute(select(AboutImage).where(AboutImage.page_id == page_id))
    ).scalars().all()
    orphans = [
        image.image_url
        for image in previous
        if image.image_url
        and image.image_url not in kept
        and not image.image_url.startswith(("http://", "https://"))
    ]

    await db.execute(sqlalchemy_delete(AboutImage).where(AboutImage.page_id == page_id))
    for index, url in rows:
        db.add(
            AboutImage(
                page_id=page_id,
                image_url=url,
                display_order=index,
                created_at=now,
                updated_at=now,
            )
        )

    for path in orphans:
        safe_delete_file(path)


async def _replace_milestones(db: AsyncSession, page_id: int, milestones: list, now: datetime):
    """Rewrites the timeline. Milestones carry no stable key, so the payload is
    the complete truth; `display_order` records the order they were sent in and
    only ever breaks ties between equal years."""
    await db.execute(
        sqlalchemy_delete(AboutMilestone).where(AboutMilestone.page_id == page_id)
    )

    for index, entry in enumerate(milestones):
        payload = entry if isinstance(entry, dict) else entry.dict(exclude_unset=True)
        milestone = AboutMilestone(
            page_id=page_id,
            year=payload.get("year"),
            display_order=index,
            created_at=now,
            updated_at=now,
        )
        db.add(milestone)
        await db.flush()
        await _upsert_translations(
            db, AboutMilestoneTr, "milestone_id", milestone.id, payload,
            MILESTONE_TR_FIELDS, now,
        )


async def _replace_pillars(db: AsyncSession, page_id: int, pillars: list, now: datetime):
    """Rewrites the pillar cards. They carry no stable key — the card's number
    is just its position — so the payload is the complete, ordered truth."""
    await db.execute(sqlalchemy_delete(AboutPillar).where(AboutPillar.page_id == page_id))

    for index, entry in enumerate(pillars):
        payload = entry if isinstance(entry, dict) else entry.dict(exclude_unset=True)
        pillar = AboutPillar(
            page_id=page_id, display_order=index, created_at=now, updated_at=now
        )
        db.add(pillar)
        await db.flush()
        await _upsert_translations(
            db, AboutPillarTr, "pillar_id", pillar.id, payload, PILLAR_TR_FIELDS, now
        )


async def _upsert_lists(db: AsyncSession, page_id: int, lists: list, now: datetime):
    """Updates the titled lists in place.

    Unlike the pillars these are matched on `list_key`, because the website
    addresses them by name (values, kpis) and the set is fixed by the page's
    design rather than by the editor.
    """
    existing = {
        entry.list_key: entry
        for entry in (
            await db.execute(select(AboutList).where(AboutList.page_id == page_id))
        ).scalars().all()
    }

    for index, entry in enumerate(lists):
        payload = entry if isinstance(entry, dict) else entry.dict(exclude_unset=True)
        key = (payload.get("list_key") or "").strip()
        if not key:
            continue

        row = existing.get(key)
        if row is None:
            row = AboutList(
                page_id=page_id, list_key=key, created_at=now, updated_at=now
            )
            db.add(row)
            await db.flush()

        if payload.get("style"):
            row.style = payload["style"]
        row.display_order = index
        row.updated_at = now
        await _upsert_translations(
            db, AboutListTr, "list_id", row.id, payload, LIST_TR_FIELDS, now
        )


async def _replace_persons(db: AsyncSession, page_id: int, persons: list, now: datetime):
    """Rewrites the vice-rector cards. They carry no stable key — a card's
    position is its identity — so the payload is the complete, ordered truth."""
    await db.execute(sqlalchemy_delete(AboutPerson).where(AboutPerson.page_id == page_id))

    for index, entry in enumerate(persons):
        payload = entry if isinstance(entry, dict) else entry.dict(exclude_unset=True)
        person = AboutPerson(page_id=page_id, display_order=index, created_at=now, updated_at=now)
        _apply(person, payload, PERSON_FIELDS)
        db.add(person)
        await db.flush()
        await _upsert_translations(
            db, AboutPersonTr, "person_id", person.id, payload, PERSON_TR_FIELDS, now
        )


async def _replace_councils(db: AsyncSession, page_id: int, councils: list, now: datetime):
    """Rewrites the scientific-board councils.

    A council and the people on it carry no stable key — position is identity —
    so the payload is the complete, ordered truth. Deleting the councils cascades
    to their members and every translation, and the whole set is recreated. Each
    council's two rosters (``members`` and ``secretaries``) are stored on one
    table, told apart by ``role``.
    """
    await db.execute(sqlalchemy_delete(AboutCouncil).where(AboutCouncil.page_id == page_id))

    for index, entry in enumerate(councils):
        payload = entry if isinstance(entry, dict) else entry.dict(exclude_unset=True)
        council = AboutCouncil(
            page_id=page_id, display_order=index, created_at=now, updated_at=now
        )
        db.add(council)
        await db.flush()
        await _upsert_translations(
            db, AboutCouncilTr, "council_id", council.id, payload, COUNCIL_TR_FIELDS, now
        )

        for role, key in ((ROLE_MEMBER, "members"), (ROLE_SECRETARY, "secretaries")):
            for order, raw in enumerate(payload.get(key) or []):
                member_payload = raw if isinstance(raw, dict) else raw.dict(exclude_unset=True)
                member = AboutCouncilMember(
                    council_id=council.id,
                    role=role,
                    display_order=order,
                    created_at=now,
                    updated_at=now,
                )
                db.add(member)
                await db.flush()
                await _upsert_translations(
                    db,
                    AboutCouncilMemberTr,
                    "member_id",
                    member.id,
                    member_payload,
                    COUNCIL_MEMBER_TR_FIELDS,
                    now,
                )


async def _replace_doc_categories(db: AsyncSession, page_id: int, categories: list, now: datetime):
    """Rewrites a regulatory-documents page's categories wholesale.

    ``category_key`` is preserved from the payload, so a document's reference to
    a category survives the save. Categories with no key are skipped.
    """
    await db.execute(
        sqlalchemy_delete(AboutDocCategory).where(AboutDocCategory.page_id == page_id)
    )
    for index, entry in enumerate(categories):
        payload = entry if isinstance(entry, dict) else entry.dict(exclude_unset=True)
        key = (payload.get("category_key") or "").strip()
        if not key:
            continue
        category = AboutDocCategory(
            page_id=page_id, category_key=key, display_order=index, created_at=now, updated_at=now
        )
        db.add(category)
        await db.flush()
        await _upsert_translations(
            db, AboutDocCategoryTr, "category_id", category.id, payload, DOC_CATEGORY_TR_FIELDS, now
        )


async def _replace_documents(db: AsyncSession, page_id: int, documents: list, now: datetime):
    """Rewrites the document cards wholesale.

    Cards carry no stable key — position is identity — so the payload is the
    complete, ordered truth. Any stored file dropped from the list is removed
    from disk so the static directory does not fill with orphans; a pasted URL
    is left alone. ``category_key`` ties a card to one of the page's categories.
    """
    rows = []
    kept: set[str] = set()
    for index, entry in enumerate(documents):
        payload = entry if isinstance(entry, dict) else entry.dict(exclude_unset=True)
        az = payload.get("az") or {}
        en = payload.get("en") or {}
        az_url = (az.get("file_url") or "").strip()
        en_url = (en.get("file_url") or "").strip()
        # Legacy top-level file_url is only a fallback for the neutral mirror.
        legacy_url = (payload.get("file_url") or "").strip()
        # Every per-language file still referenced by the new payload is kept.
        kept.update(u for u in (az_url, en_url) if u)
        # Backward-compat neutral mirror: AZ file, else EN, else any legacy value.
        mirror_url = az_url or en_url or legacy_url
        rows.append((index, payload, mirror_url))

    previous = (
        await db.execute(
            select(AboutDocument)
            .where(AboutDocument.page_id == page_id)
            .options(selectinload(AboutDocument.translations))
        )
    ).scalars().all()
    # Collect every stored path the old rows referenced — each language's tr
    # file_url plus the neutral column — so neither AZ nor EN is wrongly deleted
    # when only one of them changes. Delete a path only if the new payload no
    # longer references it in any language.
    previous_paths: set[str] = set()
    for doc in previous:
        if doc.file_url:
            previous_paths.add(doc.file_url)
        for tr in doc.translations:
            if tr.file_url:
                previous_paths.add(tr.file_url)
    orphans = [
        path
        for path in previous_paths
        if path not in kept
        and not path.startswith(("http://", "https://"))
    ]

    await db.execute(sqlalchemy_delete(AboutDocument).where(AboutDocument.page_id == page_id))
    for index, payload, mirror_url in rows:
        document = AboutDocument(
            page_id=page_id,
            category_key=(payload.get("category_key") or "").strip() or None,
            file_url=mirror_url or None,
            display_order=index,
            created_at=now,
            updated_at=now,
        )
        db.add(document)
        await db.flush()
        await _upsert_translations(
            db, AboutDocumentTr, "document_id", document.id, payload, DOCUMENT_TR_FIELDS, now
        )

    for path in orphans:
        safe_delete_file(path)


async def update_page(page_key: str, request: UpdateAboutPage, db: AsyncSession):
    try:
        page = (
            await db.execute(select(AboutPage).where(AboutPage.page_key == page_key))
        ).scalar_one_or_none()
        if page is None:
            return _error(404, "About page not found.")

        now = _now()
        data = request.dict(exclude_unset=True)

        # Replacing the portrait with a different stored file orphans the old
        # one — clean it up, but never touch a pasted URL (not ours to delete).
        if "image_url" in data:
            previous_portrait = page.image_url
            new_portrait = data["image_url"]
            if (
                previous_portrait
                and previous_portrait != new_portrait
                and not previous_portrait.startswith(("http://", "https://"))
            ):
                safe_delete_file(previous_portrait)

        for field in PAGE_FIELDS:
            if field in data:
                setattr(page, field, data[field])
        # The grade-scale table is stored inline as a list of row dicts.
        if data.get("grade_scale") is not None:
            page.grade_scale = data["grade_scale"]
        page.updated_at = now

        await _upsert_translations(
            db, AboutPageTr, "page_id", page.id, data, PAGE_TR_FIELDS, now
        )

        if data.get("blocks") is not None:
            await _replace_blocks(db, page.id, data["blocks"], now)
        if data.get("links") is not None:
            await _replace_links(db, page.id, data["links"], now)
        if data.get("milestones") is not None:
            await _replace_milestones(db, page.id, data["milestones"], now)
        if data.get("pillars") is not None:
            await _replace_pillars(db, page.id, data["pillars"], now)
        if data.get("lists") is not None:
            await _upsert_lists(db, page.id, data["lists"], now)
        if data.get("persons") is not None:
            await _replace_persons(db, page.id, data["persons"], now)
        if data.get("councils") is not None:
            await _replace_councils(db, page.id, data["councils"], now)
        if data.get("doc_categories") is not None:
            await _replace_doc_categories(db, page.id, data["doc_categories"], now)
        if data.get("documents") is not None:
            await _replace_documents(db, page.id, data["documents"], now)
        if data.get("images") is not None:
            await _replace_images(db, page.id, data["images"], now)

        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "About page updated."})
    except Exception:
        await db.rollback()
        logger.exception("Failed to update about page %s", page_key)
        return _error(500, "Failed to update about page.")


async def publish_page(page_key: str, is_active: bool, db: AsyncSession):
    """The only way a page goes live, so saving a draft can never publish it."""
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
                "status_code": status.HTTP_200_OK,
                "message": "About page published." if is_active else "About page unpublished.",
                "is_active": is_active,
            }
        )
    except Exception:
        await db.rollback()
        logger.exception("Failed to change publication state for %s", page_key)
        return _error(500, "Failed to change publication state.")


async def upload_document(page_key: str, file: UploadFile, db: AsyncSession):
    """Stores the plan file and points the page at it.

    The same column also holds a pasted URL, so uploading simply replaces
    whatever was there. Only document types are accepted — serving arbitrary
    uploads (HTML, SVG) from this domain would be an XSS vector.
    """
    try:
        page = (
            await db.execute(select(AboutPage).where(AboutPage.page_key == page_key))
        ).scalar_one_or_none()
        if page is None:
            return _error(404, "About page not found.")

        previous = page.document_url
        path = await save_upload(file, "about/documents", ALLOWED_DOC_MIMES)
        page.document_url = path
        page.updated_at = _now()
        await db.commit()

        # Only clean up a file we stored; a previously pasted URL is not ours.
        if previous and not previous.startswith(("http://", "https://")):
            safe_delete_file(previous)

        return JSONResponse(
            content={"status_code": 200, "message": "Document uploaded.", "path": path}
        )
    except Exception:
        await db.rollback()
        logger.exception("Failed to upload document for %s", page_key)
        return _error(500, "Failed to upload document.")


async def upload_image(page_key: str, file: UploadFile, db: AsyncSession):
    """Stores one image and returns its path.

    Used for both the rector's portrait and the gallery: the endpoint only
    stores the file and hands back the URL, and the whole-page save decides
    where it lands (``image_url`` or the ``images`` strip). Nothing is written
    to the page here, so an upload the editor then discards leaves no dangling
    row — only a file, which the next save's orphan sweep removes.
    """
    try:
        page = (
            await db.execute(select(AboutPage).where(AboutPage.page_key == page_key))
        ).scalar_one_or_none()
        if page is None:
            return _error(404, "About page not found.")

        path = await save_upload(file, "about/images", ALLOWED_IMAGE_MIMES)
        return JSONResponse(
            content={"status_code": 200, "message": "Image uploaded.", "path": path}
        )
    except Exception:
        logger.exception("Failed to upload image for %s", page_key)
        return _error(500, "Failed to upload image.")


async def upload_file(page_key: str, file: UploadFile, db: AsyncSession):
    """Stores one document (any supported format) and returns its path.

    The regulatory-documents pages list many downloadable files, so — like
    ``upload_image`` — this only stores the file and hands back the URL; the
    whole-page save drops the path into a document card's ``file_url``. The
    format allowlist (``ALLOWED_DOC_MIMES``) covers PDF, Office files, archives
    and plain text, and deliberately excludes HTML/SVG, which would be an XSS
    vector served from this domain.
    """
    try:
        page = (
            await db.execute(select(AboutPage).where(AboutPage.page_key == page_key))
        ).scalar_one_or_none()
        if page is None:
            return _error(404, "About page not found.")

        path = await save_upload(
            file, "about/documents", ALLOWED_DOC_MIMES, allow_extension_fallback=True
        )
        return JSONResponse(
            content={"status_code": 200, "message": "File uploaded.", "path": path}
        )
    except HTTPException as exc:
        # A bad format or oversize file — report it as-is so the dashboard can
        # tell the editor why, rather than a generic 500.
        return _error(exc.status_code, str(exc.detail))
    except Exception:
        logger.exception("Failed to upload file for %s", page_key)
        return _error(500, "Failed to upload file.")
