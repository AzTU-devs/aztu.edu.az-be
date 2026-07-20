import hashlib
from datetime import date, datetime, timedelta, timezone

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logger import get_logger
from app.models.analytics.site_visit import SiteVisitDaily, SiteVisitUnique

logger = get_logger("aztu.analytics")

# Substring match on a lowercased user agent. Deliberately broad: an
# undercounted day is better than a day whose numbers are fiction.
_BOT_MARKERS: tuple[str, ...] = (
    "bot", "crawler", "spider", "scraper", "preview", "monitor", "uptime",
    "curl", "wget", "python-requests", "httpx", "axios", "okhttp", "java/",
    "libwww", "headless", "phantomjs", "slurp", "archiver", "fetcher",
    "validator", "lighthouse", "pingdom", "semrush", "ahrefs", "facebookexternalhit",
    "whatsapp", "telegrambot", "embedly", "quora link preview", "vercel",
)

_UA_MAX = 512


def is_bot(user_agent: str | None) -> bool:
    if not user_agent:
        # No UA at all is never a real browser.
        return True
    ua = user_agent.lower()
    return any(marker in ua for marker in _BOT_MARKERS)


def client_ip(request) -> str:
    """First X-Forwarded-For entry (the origin client), else the socket peer."""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        first = forwarded_for.split(",")[0].strip()
        if first:
            return first
    real_ip = request.headers.get("X-Real-IP")
    if real_ip and real_ip.strip():
        return real_ip.strip()
    return request.client.host if request.client else "unknown"


def visitor_hash(ip: str, user_agent: str, day: date) -> str:
    """sha256(salt + ip + user agent + day).

    Including the day rotates the identifier every 24h, so a hash cannot be used
    to follow one visitor across days. Neither input is ever stored.
    """
    raw = f"{settings.VISIT_HASH_SALT}|{ip}|{user_agent[:_UA_MAX]}|{day.isoformat()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


async def record_visit(request, path: str, db: AsyncSession) -> JSONResponse:
    """Count one page view. Never raises — a tracking failure must not break a page."""
    try:
        user_agent = request.headers.get("User-Agent", "")
        if is_bot(user_agent):
            return JSONResponse(
                content={"status_code": status.HTTP_200_OK, "counted": False},
                status_code=status.HTTP_200_OK,
            )

        today = datetime.now(timezone.utc).date()
        digest = visitor_hash(client_ip(request), user_agent, today)

        await db.execute(
            pg_insert(SiteVisitDaily)
            .values(day=today, views=1)
            .on_conflict_do_update(
                index_elements=[SiteVisitDaily.day],
                set_={"views": SiteVisitDaily.views + 1},
            )
        )
        await db.execute(
            pg_insert(SiteVisitUnique)
            .values(day=today, visitor_hash=digest)
            .on_conflict_do_nothing(index_elements=["day", "visitor_hash"])
        )
        await db.commit()
    except Exception:
        # Swallowed on purpose: the public site fires this on every page view.
        logger.exception("Visit tracking failed for path=%s", (path or "")[:200])
        try:
            await db.rollback()
        except Exception:
            pass
        return JSONResponse(
            content={"status_code": status.HTTP_200_OK, "counted": False},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"status_code": status.HTTP_200_OK, "counted": True},
        status_code=status.HTTP_200_OK,
    )


async def purge_expired_site_visits() -> int:
    """Nightly retention sweep. Runs on its own session, outside any request.

    Only site_visit_unique is pruned: site_visit_daily is one row per day and is
    the long-term series the dashboards read.
    """
    from app.core.database import AsyncSessionLocal

    days = max(1, int(settings.SITE_VISIT_RETENTION_DAYS))
    cutoff = datetime.now(timezone.utc).date() - timedelta(days=days)

    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                delete(SiteVisitUnique).where(SiteVisitUnique.day < cutoff)
            )
            await db.commit()
            deleted = result.rowcount or 0
    except Exception:
        logger.exception("Site-visit retention purge failed")
        return 0

    if deleted:
        logger.info("Site-visit retention purge removed %d rows older than %s", deleted, cutoff)
    return deleted
