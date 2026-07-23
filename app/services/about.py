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

from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete as sqlalchemy_delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.v1.schema.about import UpdateAboutPage
from app.core.logger import get_logger
from app.models.about.about import (
    AboutBlock,
    AboutBlockTr,
    AboutLink,
    AboutLinkTr,
    AboutList,
    AboutListTr,
    AboutPillar,
    AboutPillarTr,
    AboutMilestone,
    AboutMilestoneTr,
    AboutPage,
    AboutPageTr,
)
from app.utils.file_upload import ALLOWED_DOC_MIMES, safe_delete_file, save_upload
from app.utils.html_sanitizer import sanitize_html

logger = get_logger(__name__)

LANGS = ("az", "en")

PAGE_TR_FIELDS = (
    "title", "description", "links_title", "document_label", "pillars_title",
)
BLOCK_TR_FIELDS = ("title", "body")
LINK_TR_FIELDS = ("label",)
MILESTONE_TR_FIELDS = ("title", "description")
PILLAR_TR_FIELDS = ("title", "description", "tags")
LIST_TR_FIELDS = ("title", "items")

# Editor-authored HTML. Scrubbed on the way in so the website can render it
# verbatim — an authenticated admin is still not a reason to store raw markup.
RICH_TEXT_FIELDS = frozenset({"description", "body"})

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


# ── Loading ────────────────────────────────────────────────────────────────────


def _page_query():
    return select(AboutPage).options(
        selectinload(AboutPage.translations),
        selectinload(AboutPage.blocks).selectinload(AboutBlock.translations),
        selectinload(AboutPage.links).selectinload(AboutLink.translations),
        selectinload(AboutPage.milestones).selectinload(AboutMilestone.translations),
        selectinload(AboutPage.pillars).selectinload(AboutPillar.translations),
        selectinload(AboutPage.lists).selectinload(AboutList.translations),
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
            for milestone in sorted(page.milestones, key=_milestone_order)
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
        "updated_at": page.updated_at.isoformat() if page.updated_at else None,
    }


def _serialize_public(page: AboutPage, lang: str) -> dict:
    copy = _pick(page.translations, lang, PAGE_TR_FIELDS)
    return {
        "page_key": page.page_key,
        "template": page.template,
        "slug": page.slug_az if lang == "az" else page.slug_en,
        "document_url": page.document_url,
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
            for milestone in sorted(page.milestones, key=_milestone_order)
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


async def update_page(page_key: str, request: UpdateAboutPage, db: AsyncSession):
    try:
        page = (
            await db.execute(select(AboutPage).where(AboutPage.page_key == page_key))
        ).scalar_one_or_none()
        if page is None:
            return _error(404, "About page not found.")

        now = _now()
        data = request.dict(exclude_unset=True)

        for field in ("slug_az", "slug_en", "document_url"):
            if field in data:
                setattr(page, field, data[field])
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
