"""Research-section service.

Two read shapes, deliberately different:

* ``get_page_admin`` returns both languages side by side plus every id, because
  the dashboard edits them together.
* ``get_page_public`` resolves one language, refuses unpublished pages, and adds
  the derived SEO fields — it is what the website consumes.

The page saves as one document. `priorities`, `patent_years` and `links` arrive
whole and replace what is stored, which matches the dashboard's single Save
button and avoids a per-row endpoint surface for a page this small.

Named ``research_page`` rather than ``research`` so it is never mistaken for the
research *institute* / *project* services, which manage entities rather than
editorial pages.
"""

import re
from datetime import datetime, timezone
from typing import Any, Iterable, Optional

from fastapi import HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete as sqlalchemy_delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.v1.schema.research import UpdateResearchPage
from app.core.logger import get_logger
from app.models.research.research import (
    ResearchPage,
    ResearchPageLink,
    ResearchPageLinkTr,
    ResearchPageTr,
    ResearchPatent,
    ResearchPatentTr,
    ResearchPatentYear,
    ResearchPriority,
    ResearchPriorityTr,
)
from app.utils.file_upload import ALLOWED_DOC_MIMES, safe_delete_file, save_upload
from app.utils.html_sanitizer import sanitize_html

logger = get_logger(__name__)

LANGS = ("az", "en")

PAGE_TR_FIELDS = ("title", "description", "body_html", "links_title")
PRIORITY_TR_FIELDS = ("title", "description")
PATENT_TR_FIELDS = ("name", "authors")
LINK_TR_FIELDS = ("label",)

# Editor-authored HTML. Scrubbed on the way in so the website can render it
# verbatim — an authenticated admin is still not a reason to store raw markup.
#
# `name` and `authors` are absent on purpose: the patents table renders them as
# plain text, so they are stored as typed and escaped by the renderer.
RICH_TEXT_FIELDS = frozenset({"description", "body_html"})

# SEO is derived here rather than typed in the dashboard: the meta description
# is the hero copy with its markup removed, clipped to a sensible length.
SEO_DESCRIPTION_LIMIT = 160

# Where patent certificates are stored, and the marker that tells one of our own
# files apart from a link an editor pasted. Written once so the upload and the
# orphan sweep cannot drift apart — if they did, the sweep would either miss
# every file or start deleting things it did not store.
UPLOAD_SUBDIR = "research/documents"
UPLOAD_DIR = f"static/{UPLOAD_SUBDIR}/"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _error(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(
        content={"status_code": status_code, "message": message}, status_code=status_code
    )


def _year_order(year_row: Any) -> tuple:
    """Oldest year first.

    Deliberately ascending, and deliberately not the editor's choice: the
    patents page reverses the list before rendering, so ascending here is what
    puts the newest year at the top of the page. Adding "2026" therefore lands
    at the top of the site with no reordering to do.

    The year is free text, so the sort reads the first 3-4 digit run out of it.
    An entry with no digits at all is malformed rather than meaningful; it sorts
    first here, which is last on the page, where it does the least harm.
    """
    match = re.search(r"\d{3,4}", year_row.year or "")
    return (int(match.group()) if match else -1, year_row.display_order)


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
    return select(ResearchPage).options(
        selectinload(ResearchPage.translations),
        selectinload(ResearchPage.priorities).selectinload(ResearchPriority.translations),
        selectinload(ResearchPage.links).selectinload(ResearchPageLink.translations),
        selectinload(ResearchPage.patent_years)
        .selectinload(ResearchPatentYear.patents)
        .selectinload(ResearchPatent.translations),
    )


async def _load_page(db: AsyncSession, page_key: str) -> Optional[ResearchPage]:
    result = await db.execute(_page_query().where(ResearchPage.page_key == page_key))
    return result.scalars().unique().one_or_none()


def _serialize_admin(page: ResearchPage) -> dict:
    return {
        "id": page.id,
        "page_key": page.page_key,
        "template": page.template,
        "slug_az": page.slug_az,
        "slug_en": page.slug_en,
        "is_active": page.is_active,
        **_tr_map(page.translations, PAGE_TR_FIELDS),
        "priorities": [
            {
                "id": priority.id,
                "display_order": priority.display_order,
                **_tr_map(priority.translations, PRIORITY_TR_FIELDS),
            }
            for priority in sorted(page.priorities, key=lambda p: p.display_order)
        ],
        "patent_years": [
            {
                "id": year_row.id,
                "year": year_row.year,
                "patents": [
                    {
                        "id": patent.id,
                        "patent_number": patent.patent_number,
                        "document_url": patent.document_url,
                        "display_order": patent.display_order,
                        **_tr_map(patent.translations, PATENT_TR_FIELDS),
                    }
                    for patent in sorted(year_row.patents, key=lambda p: p.display_order)
                ],
            }
            # Same order the website gets, so the editor is looking at the
            # stored truth rather than a second arrangement of it.
            for year_row in sorted(page.patent_years, key=_year_order)
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


def _serialize_public(page: ResearchPage, lang: str) -> dict:
    copy = _pick(page.translations, lang, PAGE_TR_FIELDS)
    return {
        "page_key": page.page_key,
        "template": page.template,
        "slug": page.slug_az if lang == "az" else page.slug_en,
        **copy,
        # Derived, not authored: the dashboard has no SEO fields by design.
        "seo": {
            "title": copy.get("title"),
            "description": _seo_description(copy.get("description")),
        },
        "priorities": [
            _pick(priority.translations, lang, PRIORITY_TR_FIELDS)
            for priority in sorted(page.priorities, key=lambda p: p.display_order)
        ],
        # Oldest year first — the patents page reverses this list before it
        # renders, so ascending here is what puts the newest year on top.
        "years": [
            {
                "year": year_row.year,
                "patents": [
                    {
                        # The row number is the position, derived rather than
                        # stored so it can never disagree with the ordering.
                        "no": str(index + 1),
                        "number": patent.patent_number,
                        "link": patent.document_url,
                        **_pick(patent.translations, lang, PATENT_TR_FIELDS),
                    }
                    for index, patent in enumerate(
                        sorted(year_row.patents, key=lambda p: p.display_order)
                    )
                ],
            }
            for year_row in sorted(page.patent_years, key=_year_order)
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
            _page_query().order_by(ResearchPage.display_order, ResearchPage.id)
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
        logger.exception("Failed to list research pages")
        return _error(500, "Failed to list research pages.")


async def get_page_admin(page_key: str, db: AsyncSession):
    try:
        page = await _load_page(db, page_key)
        if page is None:
            return _error(404, "Research page not found.")
        return JSONResponse(content={"status_code": 200, "page": _serialize_admin(page)})
    except Exception:
        logger.exception("Failed to load research page %s", page_key)
        return _error(500, "Failed to load research page.")


async def get_page_public(page_key: str, lang: str, db: AsyncSession):
    try:
        page = await _load_page(db, page_key)
        if page is None or not page.is_active:
            return _error(404, "Research page not found.")
        return JSONResponse(
            content={"status_code": 200, "page": _serialize_public(page, lang)}
        )
    except Exception:
        logger.exception("Failed to load public research page %s", page_key)
        return _error(500, "Failed to load research page.")


# ── Writes ─────────────────────────────────────────────────────────────────────


async def _replace_priorities(
    db: AsyncSession, page_id: int, priorities: list, now: datetime
):
    """Rewrites the priority cards. They carry no stable key — the card's number
    is just its position — so the payload is the complete, ordered truth."""
    await db.execute(
        sqlalchemy_delete(ResearchPriority).where(ResearchPriority.page_id == page_id)
    )

    for index, entry in enumerate(priorities):
        payload = entry if isinstance(entry, dict) else entry.dict(exclude_unset=True)
        priority = ResearchPriority(
            page_id=page_id, display_order=index, created_at=now, updated_at=now
        )
        db.add(priority)
        await db.flush()
        await _upsert_translations(
            db, ResearchPriorityTr, "priority_id", priority.id, payload,
            PRIORITY_TR_FIELDS, now,
        )


def _stored_upload(url: Optional[str]) -> bool:
    """True for a file this endpoint stored, false for a link an editor pasted.

    Matched on the directory `save_upload` writes to rather than on "is not
    http", because `save_upload` returns an absolute URL whenever
    `PUBLIC_BASE_URL` is set — a scheme test would quietly stop recognising our
    own files in exactly the deployments that have that configured.
    `safe_delete_file` independently refuses anything outside the static root.
    """
    return bool(url) and UPLOAD_DIR in url


async def _replace_patent_years(
    db: AsyncSession, page_id: int, years: list, now: datetime
) -> list:
    """Rewrites the whole patents table, years and rows together.

    Replaced wholesale rather than diffed: neither a year nor a patent row has
    an identity the editor controls, and the payload is the complete, ordered
    truth. Deleting the year cascades to its patents and their translations.

    A year with no label and no rows is an empty block the editor added and
    never filled in; it is dropped rather than stored.

    Returns the certificates that were stored here and are no longer referenced
    by anything — a replaced or deleted upload. They are not unlinked here: the
    caller does it after the commit, so a rollback can never leave a surviving
    row pointing at a file that is already gone. Uploads named with
    `secrets.token_hex` are unfindable once the last reference goes, so a sweep
    that never runs is a leak nothing can later reclaim.
    """
    kept = set()
    for year_entry in years:
        year_payload = (
            year_entry if isinstance(year_entry, dict) else year_entry.dict(exclude_unset=True)
        )
        for entry in year_payload.get("patents") or []:
            payload = entry if isinstance(entry, dict) else entry.dict(exclude_unset=True)
            url = (payload.get("document_url") or "").strip()
            if url:
                kept.add(url)

    previous = (
        await db.execute(
            select(ResearchPatent.document_url)
            .join(ResearchPatentYear, ResearchPatent.year_id == ResearchPatentYear.id)
            .where(ResearchPatentYear.page_id == page_id)
        )
    ).scalars().all()
    orphans = [
        url for url in previous if url not in kept and _stored_upload(url)
    ]

    await db.execute(
        sqlalchemy_delete(ResearchPatentYear).where(ResearchPatentYear.page_id == page_id)
    )

    for year_index, year_entry in enumerate(years):
        year_payload = (
            year_entry if isinstance(year_entry, dict) else year_entry.dict(exclude_unset=True)
        )
        patents = year_payload.get("patents") or []
        if not (year_payload.get("year") or "").strip() and not patents:
            continue

        year_row = ResearchPatentYear(
            page_id=page_id,
            year=year_payload.get("year"),
            display_order=year_index,
            created_at=now,
            updated_at=now,
        )
        db.add(year_row)
        await db.flush()

        for index, entry in enumerate(patents):
            payload = entry if isinstance(entry, dict) else entry.dict(exclude_unset=True)
            patent = ResearchPatent(
                year_id=year_row.id,
                patent_number=payload.get("patent_number"),
                document_url=payload.get("document_url"),
                display_order=index,
                created_at=now,
                updated_at=now,
            )
            db.add(patent)
            await db.flush()
            await _upsert_translations(
                db, ResearchPatentTr, "patent_id", patent.id, payload,
                PATENT_TR_FIELDS, now,
            )

    return orphans


async def _replace_links(db: AsyncSession, page_id: int, links: list, now: datetime):
    """Rewrites the button list. Buttons carry no stable key, so they are
    replaced wholesale — the payload is the complete, ordered truth."""
    await db.execute(
        sqlalchemy_delete(ResearchPageLink).where(ResearchPageLink.page_id == page_id)
    )

    for index, entry in enumerate(links):
        payload = entry if isinstance(entry, dict) else entry.dict(exclude_unset=True)
        link = ResearchPageLink(
            page_id=page_id,
            url=payload.get("url"),
            display_order=index,
            created_at=now,
            updated_at=now,
        )
        db.add(link)
        await db.flush()
        await _upsert_translations(
            db, ResearchPageLinkTr, "link_id", link.id, payload, LINK_TR_FIELDS, now
        )


async def update_page(page_key: str, request: UpdateResearchPage, db: AsyncSession):
    try:
        page = (
            await db.execute(
                select(ResearchPage).where(ResearchPage.page_key == page_key)
            )
        ).scalar_one_or_none()
        if page is None:
            return _error(404, "Research page not found.")

        now = _now()
        data = request.dict(exclude_unset=True)

        for field in ("slug_az", "slug_en"):
            if field in data:
                setattr(page, field, data[field])
        page.updated_at = now

        await _upsert_translations(
            db, ResearchPageTr, "page_id", page.id, data, PAGE_TR_FIELDS, now
        )

        orphans: list = []
        if data.get("priorities") is not None:
            await _replace_priorities(db, page.id, data["priorities"], now)
        if data.get("patent_years") is not None:
            orphans = await _replace_patent_years(db, page.id, data["patent_years"], now)
        if data.get("links") is not None:
            await _replace_links(db, page.id, data["links"], now)

        await db.commit()

        # Only after the rows are durably gone, and never inside the try that
        # could roll back: a file unlinked ahead of a failed commit would leave
        # a surviving row pointing at nothing. A failure to unlink is logged and
        # otherwise ignored — the save itself has already succeeded.
        for path in orphans:
            safe_delete_file(path)

        return JSONResponse(
            content={"status_code": 200, "message": "Research page updated."}
        )
    except Exception:
        await db.rollback()
        logger.exception("Failed to update research page %s", page_key)
        return _error(500, "Failed to update research page.")


async def publish_page(page_key: str, is_active: bool, db: AsyncSession):
    """The only way a page goes live, so saving a draft can never publish it."""
    try:
        page = (
            await db.execute(
                select(ResearchPage).where(ResearchPage.page_key == page_key)
            )
        ).scalar_one_or_none()
        if page is None:
            return _error(404, "Research page not found.")

        page.is_active = is_active
        page.updated_at = _now()
        await db.commit()

        return JSONResponse(
            content={
                "status_code": status.HTTP_200_OK,
                "message": (
                    "Research page published." if is_active else "Research page unpublished."
                ),
                "is_active": is_active,
            }
        )
    except Exception:
        await db.rollback()
        logger.exception("Failed to change publication state for %s", page_key)
        return _error(500, "Failed to change publication state.")


async def upload_document(page_key: str, file: UploadFile, db: AsyncSession):
    """Stores a certificate file and hands its path back to the dashboard.

    Deliberately writes to no row. Patent rows are replaced wholesale on save,
    so their ids do not survive one, and an upload keyed on a patent id would be
    writing to a row that the next save destroys. Instead the path travels back
    through the form and is stored by the same PUT as everything else.

    The page is still looked up so an upload cannot be aimed at a page that does
    not exist, and only document types are accepted — serving arbitrary uploads
    (HTML, SVG) from this domain would be an XSS vector.
    """
    try:
        page = (
            await db.execute(
                select(ResearchPage.id).where(ResearchPage.page_key == page_key)
            )
        ).scalar_one_or_none()
        if page is None:
            return _error(404, "Research page not found.")

        path = await save_upload(file, UPLOAD_SUBDIR, ALLOWED_DOC_MIMES)
        return JSONResponse(
            content={"status_code": 200, "message": "Document uploaded.", "path": path}
        )
    except HTTPException:
        # save_upload rejects oversized files and disallowed types with a status
        # of its own; letting it through keeps that reason visible to the editor.
        raise
    except Exception:
        logger.exception("Failed to upload document for %s", page_key)
        return _error(500, "Failed to upload document.")
