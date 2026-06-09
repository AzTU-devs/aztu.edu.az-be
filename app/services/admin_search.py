"""Admin dashboard search — queries the DB directly (no Elasticsearch).

Searches news and announcements by title across all languages in one call so
the admin can find either kind of content from a single search box. Unlike the
public ES-backed search, this includes inactive items and links to the admin
pages.
"""

from typing import Optional

from fastapi import Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.core.session import get_db
from app.models.news.news import News
from app.models.news.news_translation import NewsTranslation
from app.models.announcement.announcement import Announcement
from app.models.announcement.announcement_translation import AnnouncementTranslation

logger = get_logger(__name__)


def _like_pattern(value: str) -> str:
    """Escape LIKE wildcards so user input is matched literally (Postgres uses
    backslash as the default ILIKE escape character)."""
    escaped = value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return f"%{escaped}%"


def _pick_title(translations: dict, lang: str) -> Optional[str]:
    tr = (
        translations.get(lang)
        or translations.get("az")
        or translations.get("en")
        or next(iter(translations.values()), None)
    )
    return tr.title if tr else None


async def admin_search(
    q: str,
    lang: str = "az",
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    try:
        pattern = _like_pattern(q.strip())

        # ── News ────────────────────────────────────────────────────────────
        news_rows = (await db.execute(
            select(News)
            .join(NewsTranslation, NewsTranslation.news_id == News.news_id)
            .where(NewsTranslation.title.ilike(pattern))
            .distinct()
            .order_by(News.created_at.desc())
            .limit(limit)
        )).scalars().all()

        news_results = []
        if news_rows:
            news_ids = [n.news_id for n in news_rows]
            tr_by_news: dict[int, dict] = {}
            for tr in (await db.execute(
                select(NewsTranslation).where(NewsTranslation.news_id.in_(news_ids))
            )).scalars().all():
                tr_by_news.setdefault(tr.news_id, {})[tr.lang_code] = tr

            for n in news_rows:
                news_results.append({
                    "type": "news",
                    "id": n.news_id,
                    "title": _pick_title(tr_by_news.get(n.news_id, {}), lang),
                    "is_active": n.is_active,
                    "created_at": n.created_at.isoformat() if n.created_at else None,
                })

        # ── Announcements ───────────────────────────────────────────────────
        ann_rows = (await db.execute(
            select(Announcement)
            .join(
                AnnouncementTranslation,
                AnnouncementTranslation.announcement_id == Announcement.announcement_id,
            )
            .where(AnnouncementTranslation.title.ilike(pattern))
            .distinct()
            .order_by(Announcement.created_at.desc())
            .limit(limit)
        )).scalars().all()

        ann_results = []
        if ann_rows:
            ann_ids = [a.announcement_id for a in ann_rows]
            tr_by_ann: dict[int, dict] = {}
            for tr in (await db.execute(
                select(AnnouncementTranslation).where(
                    AnnouncementTranslation.announcement_id.in_(ann_ids)
                )
            )).scalars().all():
                tr_by_ann.setdefault(tr.announcement_id, {})[tr.lang_code] = tr

            for a in ann_rows:
                ann_results.append({
                    "type": "announcement",
                    "id": a.announcement_id,
                    "title": _pick_title(tr_by_ann.get(a.announcement_id, {}), lang),
                    "is_active": a.is_active,
                    "image": a.image,
                    "created_at": a.created_at.isoformat() if a.created_at else None,
                })

        results = news_results + ann_results
        results.sort(key=lambda r: r["created_at"] or "", reverse=True)

        return JSONResponse(
            content={
                "status_code": 200,
                "query": q,
                "results": results,
                "news": news_results,
                "announcements": ann_results,
                "total": len(results),
            }
        )

    except Exception:
        logger.exception("Failed to run admin search")
        return JSONResponse(
            content={"status_code": 500, "error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
