from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.rate_limit import limiter
from app.core.session import get_db
from app.api.v1.schema.chat import ChatRequest, ChatResponse
from app.services.chat import get_chat_reply

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
