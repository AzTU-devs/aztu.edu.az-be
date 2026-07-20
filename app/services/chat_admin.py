"""Admin-facing chatbot monitoring reads.

These endpoints return visitor IP addresses so the admin can spot abuse, which
makes every response personal data: they are gated on ``chat.read``, and each
response carries ``Cache-Control: no-store`` so no proxy or browser retains a
copy. The IP is never written to the activity log — see permission_map, where
these routes are ``no_audit``-free reads carrying no target label.
"""

from datetime import datetime, time, timedelta, timezone
from typing import Optional

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import distinct, exists, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat.chat_message import ChatMessage
from app.models.chat.chat_session import ChatSession

DEFAULT_PAGE_SIZE = 25
MAX_PAGE_SIZE = 100
TRANSCRIPT_PAGE_SIZE = 50
PREVIEW_LENGTH = 160

DAILY_BUCKETS = 30
WEEKLY_BUCKETS = 12
MONTHLY_BUCKETS = 12

SORTABLE = {
    "last_active_at": ChatSession.last_active_at,
    "started_at": ChatSession.started_at,
}

# Personal data (visitor IPs) must never land in a shared cache.
_NO_STORE = {"Cache-Control": "no-store, private", "Pragma": "no-cache"}


def _ok(data: dict) -> JSONResponse:
    return JSONResponse(
        content={"status_code": status.HTTP_200_OK, "data": data},
        status_code=status.HTTP_200_OK,
        headers=_NO_STORE,
    )


def _error(message: str, code: int) -> JSONResponse:
    return JSONResponse(
        content={"status_code": code, "message": message},
        status_code=code,
        headers=_NO_STORE,
    )


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


def _preview(content: Optional[str]) -> Optional[str]:
    if not content:
        return None
    text = " ".join(content.split())
    if len(text) <= PREVIEW_LENGTH:
        return text
    return text[:PREVIEW_LENGTH].rstrip() + "…"


def _iso(value: Optional[datetime]) -> Optional[str]:
    return value.isoformat() if value else None


async def list_chat_sessions(
    db: AsyncSession,
    page: int = 1,
    page_size: int = DEFAULT_PAGE_SIZE,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    q: Optional[str] = None,
    sort_by: str = "last_active_at",
    sort_dir: str = "desc",
) -> JSONResponse:
    page = max(1, page)
    page_size = max(1, min(page_size, MAX_PAGE_SIZE))

    filters = []

    # The range applies to last_active_at: "sessions active in this window" is
    # what abuse monitoring asks for, and it is the column the list sorts on.
    start = _day_bounds(date_from, end_of_day=False) if date_from else None
    if start:
        filters.append(ChatSession.last_active_at >= start)
    end = _day_bounds(date_to, end_of_day=True) if date_to else None
    if end:
        filters.append(ChatSession.last_active_at <= end)

    term = (q or "").strip()
    if term:
        pattern = f"%{term}%"
        filters.append(
            exists(
                select(ChatMessage.id).where(
                    ChatMessage.session_id == ChatSession.session_id,
                    ChatMessage.content.ilike(pattern),
                )
            )
        )

    count_stmt = select(func.count()).select_from(ChatSession)
    if filters:
        count_stmt = count_stmt.where(*filters)
    total = (await db.execute(count_stmt)).scalar_one()

    message_count = (
        select(func.count(ChatMessage.id))
        .where(ChatMessage.session_id == ChatSession.session_id)
        .correlate(ChatSession)
        .scalar_subquery()
    )
    first_user_message = (
        select(ChatMessage.content)
        .where(
            ChatMessage.session_id == ChatSession.session_id,
            ChatMessage.role == "user",
        )
        .order_by(ChatMessage.created_at, ChatMessage.id)
        .limit(1)
        .correlate(ChatSession)
        .scalar_subquery()
    )

    stmt = select(
        ChatSession.session_id,
        ChatSession.ip_address,
        ChatSession.started_at,
        ChatSession.last_active_at,
        message_count.label("message_count"),
        first_user_message.label("preview"),
    )
    if filters:
        stmt = stmt.where(*filters)

    column = SORTABLE.get(sort_by, ChatSession.last_active_at)
    ordering = column.asc() if sort_dir == "asc" else column.desc()
    stmt = (
        stmt.order_by(ordering, ChatSession.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    rows = (await db.execute(stmt)).all()

    items = [
        {
            "session_id": row.session_id,
            "ip_address": row.ip_address,
            "started_at": _iso(row.started_at),
            "last_active_at": _iso(row.last_active_at),
            "message_count": row.message_count or 0,
            "preview": _preview(row.preview),
        }
        for row in rows
    ]

    return _ok(
        {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "has_more": (page - 1) * page_size + len(rows) < total,
        }
    )


def _bucket(column, granularity: str):
    """date_trunc in UTC, so buckets do not drift with the server TimeZone setting."""
    return func.date_trunc(granularity, func.timezone("UTC", column))


async def _bucket_series(db: AsyncSession, granularity: str, cutoff: datetime) -> list:
    session_bucket = _bucket(ChatSession.started_at, granularity)
    session_rows = (
        await db.execute(
            select(
                session_bucket.label("bucket"),
                func.count(ChatSession.id).label("sessions"),
                func.count(distinct(ChatSession.ip_address)).label("unique_ips"),
            )
            .where(ChatSession.started_at >= cutoff)
            .group_by(session_bucket)
        )
    ).all()

    message_bucket = _bucket(ChatMessage.created_at, granularity)
    message_rows = (
        await db.execute(
            select(
                message_bucket.label("bucket"),
                func.count(ChatMessage.id).label("messages"),
            )
            .where(ChatMessage.created_at >= cutoff)
            .group_by(message_bucket)
        )
    ).all()

    merged: dict = {}
    for row in session_rows:
        merged[row.bucket] = {
            "bucket": row.bucket.date().isoformat(),
            "sessions": row.sessions,
            "unique_ips": row.unique_ips,
            "messages": 0,
        }
    for row in message_rows:
        entry = merged.get(row.bucket)
        if entry is None:
            entry = merged[row.bucket] = {
                "bucket": row.bucket.date().isoformat(),
                "sessions": 0,
                "unique_ips": 0,
                "messages": 0,
            }
        entry["messages"] = row.messages

    return [merged[key] for key in sorted(merged)]


async def get_chat_stats(db: AsyncSession) -> JSONResponse:
    now = datetime.now(timezone.utc)
    today_start = datetime.combine(now.date(), time.min, tzinfo=timezone.utc)
    day7 = now - timedelta(days=7)
    day30 = now - timedelta(days=30)

    session_totals = (
        await db.execute(
            select(
                func.count(ChatSession.id)
                .filter(ChatSession.started_at >= today_start)
                .label("today"),
                func.count(ChatSession.id)
                .filter(ChatSession.started_at >= day7)
                .label("last_7_days"),
                func.count(ChatSession.id).label("last_30_days"),
                func.count(distinct(ChatSession.ip_address))
                .filter(ChatSession.started_at >= today_start)
                .label("ips_today"),
                func.count(distinct(ChatSession.ip_address))
                .filter(ChatSession.started_at >= day7)
                .label("ips_last_7_days"),
                func.count(distinct(ChatSession.ip_address)).label("ips_last_30_days"),
            ).where(ChatSession.started_at >= day30)
        )
    ).one()

    message_totals = (
        await db.execute(
            select(
                func.count(ChatMessage.id)
                .filter(ChatMessage.created_at >= today_start)
                .label("today"),
                func.count(ChatMessage.id)
                .filter(ChatMessage.created_at >= day7)
                .label("last_7_days"),
                func.count(ChatMessage.id).label("last_30_days"),
            ).where(ChatMessage.created_at >= day30)
        )
    ).one()

    all_time = (
        await db.execute(
            select(
                select(func.count(ChatSession.id)).scalar_subquery().label("sessions"),
                select(func.count(ChatMessage.id)).scalar_subquery().label("messages"),
                select(func.count(distinct(ChatSession.ip_address)))
                .scalar_subquery()
                .label("unique_ips"),
            )
        )
    ).one()

    daily = await _bucket_series(db, "day", now - timedelta(days=DAILY_BUCKETS))
    weekly = await _bucket_series(db, "week", now - timedelta(weeks=WEEKLY_BUCKETS))
    monthly = await _bucket_series(db, "month", now - timedelta(days=MONTHLY_BUCKETS * 31))

    return _ok(
        {
            "generated_at": _iso(now),
            "totals": {
                "today": {
                    "sessions": session_totals.today,
                    "messages": message_totals.today,
                    "unique_ips": session_totals.ips_today,
                },
                "last_7_days": {
                    "sessions": session_totals.last_7_days,
                    "messages": message_totals.last_7_days,
                    "unique_ips": session_totals.ips_last_7_days,
                },
                "last_30_days": {
                    "sessions": session_totals.last_30_days,
                    "messages": message_totals.last_30_days,
                    "unique_ips": session_totals.ips_last_30_days,
                },
                "all_time": {
                    "sessions": all_time.sessions,
                    "messages": all_time.messages,
                    "unique_ips": all_time.unique_ips,
                },
            },
            "daily": daily,
            "weekly": weekly,
            "monthly": monthly,
            "series": daily,
        }
    )


async def get_chat_transcript(
    db: AsyncSession,
    session_id: str,
    page: int = 1,
    page_size: int = TRANSCRIPT_PAGE_SIZE,
) -> JSONResponse:
    page = max(1, page)
    page_size = max(1, min(page_size, MAX_PAGE_SIZE))

    session = (
        await db.execute(
            select(ChatSession).where(ChatSession.session_id == session_id)
        )
    ).scalar_one_or_none()
    if session is None:
        return _error("Söhbət tapılmadı.", status.HTTP_404_NOT_FOUND)

    total = (
        await db.execute(
            select(func.count(ChatMessage.id)).where(
                ChatMessage.session_id == session_id
            )
        )
    ).scalar_one()

    rows = (
        (
            await db.execute(
                select(ChatMessage)
                .where(ChatMessage.session_id == session_id)
                .order_by(ChatMessage.created_at, ChatMessage.id)
                .offset((page - 1) * page_size)
                .limit(page_size)
            )
        )
        .scalars()
        .all()
    )

    return _ok(
        {
            "session": {
                "session_id": session.session_id,
                "ip_address": session.ip_address,
                "started_at": _iso(session.started_at),
                "last_active_at": _iso(session.last_active_at),
                "message_count": total,
            },
            "items": [
                {
                    "id": row.id,
                    "role": row.role,
                    "content": row.content,
                    "created_at": _iso(row.created_at),
                }
                for row in rows
            ],
            "total": total,
            "page": page,
            "page_size": page_size,
            "has_more": (page - 1) * page_size + len(rows) < total,
        }
    )


async def delete_chat_session(db: AsyncSession, session_id: str) -> JSONResponse:
    """Delete one conversation together with its messages.

    Deliberately two Core DELETEs rather than ``db.delete(session)``.
    ``ChatSession.messages`` declares no ``cascade`` and no ``passive_deletes``,
    so the ORM path loads the children and NULLs their ``session_id`` — which the
    NOT NULL constraint rejects. Deleting the messages explicitly also means this
    does not depend on the live table actually carrying the ON DELETE CASCADE the
    model declares, which has not always held on this database.
    """
    exists_row = (
        await db.execute(
            select(ChatSession.id).where(ChatSession.session_id == session_id)
        )
    ).scalar_one_or_none()
    if exists_row is None:
        return _error("Söhbət tapılmadı.", status.HTTP_404_NOT_FOUND)

    message_count = (
        await db.execute(
            select(func.count(ChatMessage.id)).where(
                ChatMessage.session_id == session_id
            )
        )
    ).scalar_one()

    await db.execute(
        sqlalchemy_delete(ChatMessage).where(ChatMessage.session_id == session_id)
    )
    await db.execute(
        sqlalchemy_delete(ChatSession).where(ChatSession.session_id == session_id)
    )
    await db.commit()

    return _ok({"session_id": session_id, "deleted_messages": message_count})
