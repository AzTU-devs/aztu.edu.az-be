"""Admin dashboard aggregate.

One response, five round trips. Every number is a SQL ``count(*)``; nothing is
counted by loading rows and calling ``len()``. The per-entity counts, the
publishing trend and the visitor series are each folded into a single statement
with ``UNION ALL`` / ``GROUP BY`` rather than one query per metric.
"""

import logging
from datetime import date, datetime, timedelta, timezone

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import String, cast, func, literal, select, union_all
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admin.activity_log import AdminActivityLog
from app.models.admin.admin_user import AdminUser
from app.models.analytics.site_visit import SiteVisitDaily, SiteVisitUnique
from app.models.announcement.announcement import Announcement
from app.models.cafedras.cafedra_section import CafedraLaboratory
from app.models.cafedras.cafedras import Cafedra
from app.models.collaboration.collaboration import Collaboration
from app.models.employee.employee import Employee
from app.models.faculties.faculties import Faculty
from app.models.faculties.faculty_section import FacultyLaboratory
from app.models.hero.hero import Hero
from app.models.menu.footer import MenuFooterLink
from app.models.menu.header import MenuHeaderItem
from app.models.news.news import News
from app.models.news_gallery.news_gallery import NewsGallery
from app.models.project.project import Project
from app.models.research_institute.institute import ResearchInstitute
from app.services.activity import _row_payload

logger = logging.getLogger("aztu.dashboard")

DEFAULT_ACTIVITY_LIMIT = 10
MAX_ACTIVITY_LIMIT = 50

TREND_MONTHS = 12
VISIT_SERIES_DAYS = 30

# Every metric that is a plain row count, resolved in one UNION ALL.
# (key, model) — order here is the order the buckets are read back into.
_CONTENT_COUNTS = (
    ("news", News),
    ("announcements", Announcement),
    ("projects", Project),
    ("sliders", Hero),
    ("gallery_images", NewsGallery),
    ("header_menu_items", MenuHeaderItem),
    ("footer_menu_items", MenuFooterLink),
    ("collaborators", Collaboration),
)

_ACADEMIC_COUNTS = (
    ("faculties", Faculty),
    ("cafedras", Cafedra),
    ("employees", Employee),
    ("research_institutes", ResearchInstitute),
)

# "Research laboratories" is not one table: labs hang off both faculties and
# cafedras, so the dashboard figure is the sum of the two.
_LAB_COUNTS = (
    ("research_laboratories", FacultyLaboratory),
    ("research_laboratories", CafedraLaboratory),
)

# Only entities carrying created_at can be plotted over time. news_gallery,
# menu_header_items and menu_footer_links have no timestamp column, so they are
# counted above but deliberately absent from the trend.
_TREND_ENTITIES = (
    ("news", News),
    ("announcements", Announcement),
    ("projects", Project),
    ("sliders", Hero),
    ("collaborators", Collaboration),
)


def _month_keys(today: date) -> list:
    """The last TREND_MONTHS calendar months, oldest first, as 'YYYY-MM'."""
    cursor = today.replace(day=1)
    months = []
    for _ in range(TREND_MONTHS):
        months.append(cursor)
        cursor = (cursor - timedelta(days=1)).replace(day=1)
    months.reverse()
    return months


async def _counts(db: AsyncSession) -> dict:
    """Every plain row count in one statement."""
    parts = [
        select(cast(literal(key), String).label("bucket"), func.count().label("total")).select_from(model)
        for key, model in (*_CONTENT_COUNTS, *_ACADEMIC_COUNTS, *_LAB_COUNTS)
    ]
    parts.append(
        select(cast(literal("admins_total"), String), func.count()).select_from(AdminUser)
    )
    parts.append(
        select(cast(literal("admins_active"), String), func.count())
        .select_from(AdminUser)
        .where(AdminUser.is_active.is_(True))
    )

    rows = (await db.execute(union_all(*parts))).all()

    totals: dict = {}
    for bucket, total in rows:
        totals[bucket] = totals.get(bucket, 0) + int(total or 0)
    return totals


async def _publishing_trend(db: AsyncSession, months: list) -> dict:
    """One grouped query per entity, all unioned into a single round trip."""
    window_start = datetime.combine(months[0], datetime.min.time(), tzinfo=timezone.utc)

    parts = []
    for key, model in _TREND_ENTITIES:
        bucket = func.to_char(func.date_trunc("month", model.created_at), "YYYY-MM")
        parts.append(
            select(
                cast(literal(key), String).label("entity"),
                bucket.label("month"),
                func.count().label("total"),
            )
            .select_from(model)
            .where(model.created_at >= window_start)
            .group_by(bucket)
        )

    rows = (await db.execute(union_all(*parts))).all()

    labels = [month.strftime("%Y-%m") for month in months]
    index = {label: position for position, label in enumerate(labels)}
    series = {key: [0] * len(labels) for key, _ in _TREND_ENTITIES}

    for entity, month, total in rows:
        position = index.get(month)
        if position is not None:
            series[entity][position] = int(total or 0)

    return {
        "months": labels,
        "series": [
            {"key": key, "data": series[key], "total": sum(series[key])}
            for key, _ in _TREND_ENTITIES
        ],
    }


async def _visitors(db: AsyncSession, today: date) -> dict:
    """Two queries: the daily view counters, and uniques grouped per day.

    The 30-day window is fetched once and the today / 7-day / 30-day totals are
    summed from it, so the shorter ranges cost no extra round trips.
    """
    window_start = today - timedelta(days=VISIT_SERIES_DAYS - 1)

    view_rows = (
        await db.execute(
            select(SiteVisitDaily.day, SiteVisitDaily.views).where(
                SiteVisitDaily.day >= window_start
            )
        )
    ).all()
    unique_rows = (
        await db.execute(
            select(SiteVisitUnique.day, func.count())
            .where(SiteVisitUnique.day >= window_start)
            .group_by(SiteVisitUnique.day)
        )
    ).all()

    views_by_day = {row[0]: int(row[1] or 0) for row in view_rows}
    uniques_by_day = {row[0]: int(row[1] or 0) for row in unique_rows}

    days = [window_start + timedelta(days=offset) for offset in range(VISIT_SERIES_DAYS)]
    series = [
        {
            "day": day.isoformat(),
            "views": views_by_day.get(day, 0),
            "uniques": uniques_by_day.get(day, 0),
        }
        for day in days
    ]

    def _window(size: int) -> dict:
        recent = days[-size:]
        return {
            "views": sum(views_by_day.get(day, 0) for day in recent),
            "uniques": sum(uniques_by_day.get(day, 0) for day in recent),
        }

    return {
        "today": {
            "views": views_by_day.get(today, 0),
            "uniques": uniques_by_day.get(today, 0),
        },
        "last_7_days": _window(7),
        "last_30_days": _window(VISIT_SERIES_DAYS),
        "daily": series,
    }


async def _section(db: AsyncSession, name: str, coro, fallback, unavailable: list):
    """Run one panel's query, degrading that panel alone if it fails.

    A dashboard should not go blank because a single table is missing — that is
    exactly what happened when admin_activity_log had not been migrated yet. The
    rollback is required, not defensive: in PostgreSQL a failed statement aborts
    the surrounding transaction, so without it every later panel fails too.
    Failures are reported in ``unavailable`` rather than swallowed into zeros,
    which would read as real data.
    """
    try:
        return await coro
    except Exception:
        logger.exception("Dashboard section %r failed", name)
        await db.rollback()
        unavailable.append(name)
        return fallback


async def _recent_activity(db: AsyncSession, limit: int):
    return (
        await db.execute(
            select(AdminActivityLog)
            .order_by(AdminActivityLog.created_at.desc(), AdminActivityLog.id.desc())
            .limit(limit)
        )
    ).scalars().all()


async def get_dashboard_stats(db: AsyncSession, activity_limit: int = DEFAULT_ACTIVITY_LIMIT) -> JSONResponse:
    activity_limit = max(1, min(activity_limit, MAX_ACTIVITY_LIMIT))
    today = datetime.now(timezone.utc).date()
    months = _month_keys(today)
    unavailable: list = []

    totals = await _section(db, "counts", _counts(db), {}, unavailable)
    recent_rows = await _section(
        db, "activity", _recent_activity(db, activity_limit), [], unavailable
    )
    trend = await _section(db, "publishing_trend", _publishing_trend(db, months), [], unavailable)
    visitors = await _section(db, "visitors", _visitors(db, today), None, unavailable)

    return JSONResponse(
        content={
            "status_code": status.HTTP_200_OK,
            "data": {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "content": {key: totals.get(key, 0) for key, _ in _CONTENT_COUNTS},
                "academic": {
                    **{key: totals.get(key, 0) for key, _ in _ACADEMIC_COUNTS},
                    "research_laboratories": totals.get("research_laboratories", 0),
                },
                "admins": {
                    "total": totals.get("admins_total", 0),
                    "active": totals.get("admins_active", 0),
                    "recent_activity": [_row_payload(row) for row in recent_rows],
                },
                "publishing_trend": trend,
                "visitors": visitors,
                # Names the panels whose query failed, so the UI can say "could
                # not load" for those instead of rendering a confident zero.
                "unavailable": unavailable,
            },
        },
        status_code=status.HTTP_200_OK,
    )
