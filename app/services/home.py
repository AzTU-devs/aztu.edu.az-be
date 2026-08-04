"""Home-section service.

The homepage is a singleton (``page_key = "home"``) carrying two ordered metric
strips — a compact "hero" row of headline rankings and a longer "numbers" grid —
stored on one table and told apart by a neutral ``group`` column.

Two read shapes, deliberately different (mirroring About):

* ``get_page_admin`` returns both languages side by side plus every id, because
  the dashboard edits them together.
* ``get_page_public`` resolves one language and refuses an unpublished page — it
  is what the website consumes.

The page saves as one document: ``hero_metrics`` and ``number_metrics`` arrive
whole and each replaces the rows of its own group, which matches the dashboard's
single Save button and avoids a per-row endpoint surface for a page this small.
"""

from datetime import datetime, timezone
from typing import Any, Iterable, Optional

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import delete as sqlalchemy_delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.v1.schema.home import UpdateHomePage
from app.core.logger import get_logger
from app.models.home.home import HomeMetric, HomeMetricTr, HomePage

logger = get_logger(__name__)

LANGS = ("az", "en")

METRIC_TR_FIELDS = ("label", "sublabel")

GROUP_HERO = "hero"
GROUP_NUMBERS = "numbers"


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
                    getattr(model, fk_name) == fk_value, model.lang_code == lang
                )
            )
        ).scalar_one_or_none()

        if existing is None:
            existing = model(**{fk_name: fk_value}, lang_code=lang)
            db.add(existing)

        _apply(existing, tr_data, fields)


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
    return select(HomePage).options(
        selectinload(HomePage.metrics).selectinload(HomeMetric.translations),
    )


async def _load_page(db: AsyncSession, page_key: str) -> Optional[HomePage]:
    result = await db.execute(_page_query().where(HomePage.page_key == page_key))
    return result.scalars().unique().one_or_none()


def _metrics_of(page: HomePage, group: str) -> list:
    return sorted(
        (m for m in page.metrics if m.group == group),
        key=lambda m: m.display_order,
    )


def _serialize_admin(page: HomePage) -> dict:
    def admin_list(group: str) -> list:
        return [
            {
                "id": metric.id,
                "display_order": metric.display_order,
                "value": metric.value,
                "suffix": metric.suffix,
                **_tr_map(metric.translations, METRIC_TR_FIELDS),
            }
            for metric in _metrics_of(page, group)
        ]

    return {
        "id": page.id,
        "page_key": page.page_key,
        "is_active": page.is_active,
        "hero_metrics": admin_list(GROUP_HERO),
        "number_metrics": admin_list(GROUP_NUMBERS),
        "updated_at": page.updated_at.isoformat() if page.updated_at else None,
    }


def _serialize_public(page: HomePage, lang: str) -> dict:
    def hero_list() -> list:
        out = []
        for metric in _metrics_of(page, GROUP_HERO):
            picked = _pick(metric.translations, lang, METRIC_TR_FIELDS)
            out.append(
                {
                    "value": metric.value,
                    "suffix": metric.suffix,
                    "label": picked.get("label"),
                }
            )
        return out

    def number_list() -> list:
        out = []
        for metric in _metrics_of(page, GROUP_NUMBERS):
            picked = _pick(metric.translations, lang, METRIC_TR_FIELDS)
            out.append(
                {
                    "value": metric.value,
                    "suffix": metric.suffix,
                    "label": picked.get("label"),
                    "sublabel": picked.get("sublabel"),
                }
            )
        return out

    return {
        "page_key": page.page_key,
        "is_active": page.is_active,
        "hero_metrics": hero_list(),
        "number_metrics": number_list(),
    }


# ── Reads ──────────────────────────────────────────────────────────────────────


async def get_page_admin(page_key: str, db: AsyncSession):
    try:
        page = await _load_page(db, page_key)
        if page is None:
            return _error(404, "Home page not found.")
        return JSONResponse(content={"status_code": 200, "page": _serialize_admin(page)})
    except Exception:
        logger.exception("Failed to load home page %s", page_key)
        return _error(500, "Failed to load home page.")


async def get_page_public(page_key: str, lang: str, db: AsyncSession):
    try:
        page = await _load_page(db, page_key)
        if page is None or not page.is_active:
            return _error(404, "Home page not found.")
        return JSONResponse(
            content={"status_code": 200, "page": _serialize_public(page, lang)}
        )
    except Exception:
        logger.exception("Failed to load public home page %s", page_key)
        return _error(500, "Failed to load home page.")


# ── Writes ─────────────────────────────────────────────────────────────────────


async def _replace_metrics(
    db: AsyncSession, page_id: int, group: str, metrics: list, now: datetime
):
    """Rewrites one group's metric strip in the order given.

    Only the rows of this ``group`` are deleted and recreated — the other strip
    is left untouched — so ``hero_metrics`` and ``number_metrics`` can be saved
    independently. Metrics carry no stable key (position is identity), so the
    payload is the complete, ordered truth for the group.
    """
    await db.execute(
        sqlalchemy_delete(HomeMetric).where(
            HomeMetric.page_id == page_id, HomeMetric.group == group
        )
    )

    for index, entry in enumerate(metrics):
        payload = entry if isinstance(entry, dict) else entry.dict(exclude_unset=True)
        metric = HomeMetric(
            page_id=page_id,
            group=group,
            value=payload.get("value"),
            suffix=payload.get("suffix"),
            display_order=index,
            created_at=now,
            updated_at=now,
        )
        db.add(metric)
        await db.flush()
        await _upsert_translations(
            db, HomeMetricTr, "metric_id", metric.id, payload, METRIC_TR_FIELDS, now
        )


async def update_page(page_key: str, request: UpdateHomePage, db: AsyncSession):
    try:
        page = (
            await db.execute(select(HomePage).where(HomePage.page_key == page_key))
        ).scalar_one_or_none()
        if page is None:
            return _error(404, "Home page not found.")

        now = _now()
        data = request.dict(exclude_unset=True)

        if "hero_metrics" in data:
            await _replace_metrics(db, page.id, GROUP_HERO, data["hero_metrics"] or [], now)
        if "number_metrics" in data:
            await _replace_metrics(db, page.id, GROUP_NUMBERS, data["number_metrics"] or [], now)

        page.updated_at = now
        await db.commit()
        return JSONResponse(content={"status_code": 200, "message": "Home page updated."})
    except Exception:
        await db.rollback()
        logger.exception("Failed to update home page %s", page_key)
        return _error(500, "Failed to update home page.")


async def publish_page(page_key: str, is_active: bool, db: AsyncSession):
    """The only way the page goes live, so saving a draft can never publish it."""
    try:
        page = (
            await db.execute(select(HomePage).where(HomePage.page_key == page_key))
        ).scalar_one_or_none()
        if page is None:
            return _error(404, "Home page not found.")

        page.is_active = is_active
        page.updated_at = _now()
        await db.commit()

        return JSONResponse(
            content={
                "status_code": status.HTTP_200_OK,
                "message": "Home page published." if is_active else "Home page unpublished.",
                "is_active": is_active,
            }
        )
    except Exception:
        await db.rollback()
        logger.exception("Failed to change publication state for %s", page_key)
        return _error(500, "Failed to change publication state.")
