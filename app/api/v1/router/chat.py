from fastapi import APIRouter, Request
from app.core.rate_limit import limiter
from app.api.v1.schema.chat import ChatRequest, ChatResponse
from app.services.chat import get_chat_reply

router = APIRouter()


@router.post("/message", response_model=ChatResponse)
@limiter.limit("20/minute")
async def chat_message(request: Request, body: ChatRequest):
    reply = await get_chat_reply(body.message)
    return ChatResponse(reply=reply)
