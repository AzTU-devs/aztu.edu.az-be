"""Activity-log reads.

Messages are rendered here, at read time, from ``action_key`` + ``target_label``.
Nothing human-readable is stored, so wording can be corrected with no backfill.
"""

from datetime import datetime, time, timezone
from typing import Optional

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import delete, func, or_, select

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.audit_labels import action_label, render_message
from app.core.audit_payload import classify_client
from app.core.logger import get_logger
from app.models.admin.activity_log import AdminActivityLog
from app.models.admin.admin_user import AdminUser
from app.core.permissions import DOMAIN_LABELS, DOMAIN_ORDER

logger = get_logger(__name__)

DEFAULT_PAGE_SIZE = 25
MAX_PAGE_SIZE = 100


def _error(message: str, code: int) -> JSONResponse:
    return JSONResponse(content={"status_code": code, "message": message}, status_code=code)


def _row_payload(row: AdminActivityLog) -> dict:
    return {
        "id": row.id,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "admin_user_id": row.admin_user_id,
        "admin_username": row.admin_username,
        "action_key": row.action_key,
        "domain": row.domain,
        "message_az": render_message(row, "az"),
        "message_en": render_message(row, "en"),
        "target_type": row.target_type,
        "target_id": row.target_id,
        "target_label": row.target_label,
        "method": row.method,
        "path": row.path,
        "status_code": row.status_code,
        "outcome": row.outcome,
        "ip": row.ip,
        "user_agent": row.user_agent,
        # Derived at read time, never stored: the classification can be improved
        # later without a backfill, and it is only ever what the caller claimed.
        "client": classify_client(row.user_agent),
        "request_id": row.request_id,
        "request_body": row.request_body,
        "response_body": row.response_body,
        "meta": row.meta,
    }


def _day_bounds(value: str, end_of_day: bool) -> Optional[datetime]:
    """Accept a bare date ("2026-07-01") or a full ISO timestamp."""
    raw = (value or "").strip()
    if not raw:
        return None
    try:
        if len(raw) == 10:
            parsed = datetime.fromisoformat(raw)
            moment = time.max if end_of_day else time.min
            return datetime.combine(parsed.date(), moment, tzinfo=timezone.utc)
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


async def list_activity(
    db: AsyncSession,
    page: int = 1,
    page_size: int = DEFAULT_PAGE_SIZE,
    admin_user_id: Optional[int] = None,
    domain: Optional[str] = None,
    action_key: Optional[str] = None,
    outcome: Optional[str] = None,
    target_type: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    q: Optional[str] = None,
) -> JSONResponse:
    page = max(1, page)
    page_size = max(1, min(page_size, MAX_PAGE_SIZE))

    filters = []
    if admin_user_id:
        filters.append(AdminActivityLog.admin_user_id == admin_user_id)
    if domain:
        filters.append(AdminActivityLog.domain == domain)
    if action_key:
        filters.append(AdminActivityLog.action_key == action_key)
    if outcome:
        filters.append(AdminActivityLog.outcome == outcome)
    if target_type:
        filters.append(AdminActivityLog.target_type == target_type)

    start = _day_bounds(date_from, end_of_day=False) if date_from else None
    if start:
        filters.append(AdminActivityLog.created_at >= start)
    end = _day_bounds(date_to, end_of_day=True) if date_to else None
    if end:
        filters.append(AdminActivityLog.created_at <= end)

    term = (q or "").strip()
    if term:
        # The message is not stored, so free text searches the fields it is built
        # from plus the resolved record name.
        pattern = f"%{term}%"
        filters.append(
            or_(
                AdminActivityLog.admin_username.ilike(pattern),
                AdminActivityLog.target_label.ilike(pattern),
                AdminActivityLog.action_key.ilike(pattern),
                AdminActivityLog.path.ilike(pattern),
            )
        )

    count_stmt = select(func.count()).select_from(AdminActivityLog)
    if filters:
        count_stmt = count_stmt.where(*filters)
    total = (await db.execute(count_stmt)).scalar_one()

    stmt = select(AdminActivityLog)
    if filters:
        stmt = stmt.where(*filters)
    stmt = (
        stmt.order_by(AdminActivityLog.created_at.desc(), AdminActivityLog.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    rows = (await db.execute(stmt)).scalars().all()

    return JSONResponse(
        content={
            "status_code": status.HTTP_200_OK,
            "data": {
                "items": [_row_payload(row) for row in rows],
                "total": total,
                "page": page,
                "page_size": page_size,
                "has_more": (page - 1) * page_size + len(rows) < total,
            },
        },
        status_code=status.HTTP_200_OK,
    )


async def get_activity_filters(db: AsyncSession) -> JSONResponse:
    """Everything the filter bar needs in one call.

    ``admins`` lists every admin user, not only those with rows in the log, because
    it doubles as the "last login per admin" panel the super admin asked for — an
    admin who has never signed in is exactly the entry worth seeing there.
    """
    admin_rows = (
        await db.execute(
            select(
                AdminUser.id,
                AdminUser.username,
                AdminUser.is_active,
                AdminUser.last_login_at,
            ).order_by(AdminUser.username)
        )
    ).all()

    admins = [
        {
            "id": row.id,
            "username": row.username,
            "is_active": bool(row.is_active),
            "last_login_at": row.last_login_at.isoformat() if row.last_login_at else None,
        }
        for row in admin_rows
    ]

    used_domains = {
        value
        for (value,) in (await db.execute(select(AdminActivityLog.domain).distinct())).all()
        if value
    }
    domains = [
        {
            "key": key,
            "label_az": DOMAIN_LABELS[key][0],
            "label_en": DOMAIN_LABELS[key][1],
        }
        for key in DOMAIN_ORDER
        if key in used_domains
    ]
    # Domains recorded before a catalogue rename still deserve a filter entry.
    domains.extend(
        {"key": key, "label_az": key, "label_en": key}
        for key in sorted(used_domains - set(DOMAIN_ORDER))
    )

    used_actions = sorted(
        value
        for (value,) in (await db.execute(select(AdminActivityLog.action_key).distinct())).all()
        if value
    )
    actions = [
        {
            "key": key,
            "label_az": action_label(key, "az"),
            "label_en": action_label(key, "en"),
        }
        for key in used_actions
    ]

    return JSONResponse(
        content={
            "status_code": status.HTTP_200_OK,
            "data": {"admins": admins, "domains": domains, "actions": actions},
        },
        status_code=status.HTTP_200_OK,
    )


async def purge_expired_activity() -> int:
    """Nightly retention sweep. Runs on its own session, outside any request."""
    from datetime import timedelta

    from app.core.config import settings
    from app.core.database import AsyncSessionLocal

    days = max(1, int(settings.AUDIT_LOG_RETENTION_DAYS))
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                delete(AdminActivityLog).where(AdminActivityLog.created_at < cutoff)
            )
            await db.commit()
            deleted = result.rowcount or 0
    except Exception:
        logger.exception("Activity-log retention purge failed")
        return 0

    if deleted:
        logger.info("Activity-log retention purge removed %d rows older than %s", deleted, cutoff.date())
    return deleted
