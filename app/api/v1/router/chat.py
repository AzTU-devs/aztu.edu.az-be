from typing import Optional

from fastapi import APIRouter, Request, Response, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth_dependency import require_admin
from app.core.rate_limit import limiter
from app.core.session import get_db
from app.api.v1.schema.chat import ChatRequest, ChatResponse
from app.models.admin.admin_user import AdminUser
from app.services.chat import get_chat_reply
from app.services.chat_admin import (
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    TRANSCRIPT_PAGE_SIZE,
    get_chat_stats,
    get_chat_transcript,
    list_chat_sessions,
)

router = APIRouter()


def _get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@router.post("/message", response_model=ChatResponse)
@limiter.limit("20/minute")
async def chat_message(
    request: Request,
    response: Response,
    body: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    ip = _get_client_ip(request)
    reply, session_id = await get_chat_reply(
        message=body.message,
        session_id=body.session_id,
        ip_address=ip,
        db=db,
    )
    return ChatResponse(reply=reply, session_id=session_id)


@router.get("/admin/sessions")
async def list_chat_sessions_endpoint(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    date_from: Optional[str] = Query(default=None),
    date_to: Optional[str] = Query(default=None),
    q: Optional[str] = Query(default=None),
    sort_by: str = Query(default="last_active_at"),
    sort_dir: str = Query(default="desc", pattern="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await list_chat_sessions(
        db=db,
        page=page,
        page_size=page_size,
        date_from=date_from,
        date_to=date_to,
        q=q,
        sort_by=sort_by,
        sort_dir=sort_dir,
    )


@router.get("/admin/stats")
async def get_chat_stats_endpoint(
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_chat_stats(db=db)


@router.get("/admin/sessions/{session_id}/messages")
async def get_chat_transcript_endpoint(
    session_id: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=TRANSCRIPT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_chat_transcript(
        db=db, session_id=session_id, page=page, page_size=page_size
    )
