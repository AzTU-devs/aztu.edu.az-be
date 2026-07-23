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

from fastapi import status
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
    AboutPage,
    AboutPageTr,
)
from app.utils.html_sanitizer import sanitize_html

logger = get_logger(__name__)

LANGS = ("az", "en")

PAGE_TR_FIELDS = ("title", "description", "links_title")
BLOCK_TR_FIELDS = ("title", "body")
LINK_TR_FIELDS = ("label",)

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
    )


async def _load_page(db: AsyncSession, page_key: str) -> Optional[AboutPage]:
    result = await db.execute(_page_query().where(AboutPage.page_key == page_key))
    return result.scalars().unique().one_or_none()


def _serialize_admin(page: AboutPage) -> dict:
    return {
        "id": page.id,
        "page_key": page.page_key,
        "slug_az": page.slug_az,
        "slug_en": page.slug_en,
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
        "updated_at": page.updated_at.isoformat() if page.updated_at else None,
    }


def _serialize_public(page: AboutPage, lang: str) -> dict:
    copy = _pick(page.translations, lang, PAGE_TR_FIELDS)
    return {
        "page_key": page.page_key,
        "slug": page.slug_az if lang == "az" else page.slug_en,
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


async def update_page(page_key: str, request: UpdateAboutPage, db: AsyncSession):
    try:
        page = (
            await db.execute(select(AboutPage).where(AboutPage.page_key == page_key))
        ).scalar_one_or_none()
        if page is None:
            return _error(404, "About page not found.")

        now = _now()
        data = request.dict(exclude_unset=True)

        for field in ("slug_az", "slug_en"):
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
