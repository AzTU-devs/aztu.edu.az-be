import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from openai import AsyncOpenAI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.chat.chat_session import ChatSession
from app.models.chat.chat_message import ChatMessage

_SYSTEM_PROMPT = """You are the official AI assistant of Azerbaijan Technical University (AzTU).
Your sole purpose is to answer questions strictly using the AZTU KNOWLEDGE BASE
provided below. Do not rely on your own training data for AzTU facts.

STRICT OPERATING RULES:
1. ONLY answer questions directly related to Azerbaijan Technical University.
2. ONLY use facts present in the AZTU KNOWLEDGE BASE below. If the answer is
   not in the knowledge base, reply (in the user's language) that you do not
   have that information.
3. For ANY question outside the AzTU scope, politely refuse by saying:
   "I am designed to assist only with questions regarding Azerbaijan Technical University."
4. CONTENT SAFETY: Do not respond to profanity, insults, hate speech, or offensive language.
   If the user uses such language, state that you cannot assist with requests of that nature.
5. Do not engage in casual conversation or answer non-university related prompts.
6. MAXIMUM response length: 500 characters. Shorter is better.
7. Always respond in the same language the user used (Azerbaijani or English)."""

_KB_PATH = Path(__file__).resolve().parents[2] / "aztu_knowledge_base.md"


def _load_static_knowledge() -> str:
    if _KB_PATH.exists():
        return _KB_PATH.read_text(encoding="utf-8")
    return ""


# Parsed once per process (i.e. per deploy). Restart the service to pick up
# changes to aztu_knowledge_base.md.
_STATIC_KNOWLEDGE: str = _load_static_knowledge()


async def get_chat_reply(
    message: str,
    session_id: Optional[str],
    ip_address: str,
    db: AsyncSession,
) -> tuple[str, str]:
    # ── Resolve or create session ────────────────────────────────────────────
    session: Optional[ChatSession] = None

    if session_id:
        result = await db.execute(
            select(ChatSession).where(ChatSession.session_id == session_id)
        )
        session = result.scalar_one_or_none()
        # Bind sessions to their originating IP so a stolen session_id from
        # one client cannot be replayed from another IP to read or extend
        # someone else's chat history.
        if session is not None and session.ip_address != ip_address:
            session = None

    if session is None:
        session_id = str(uuid.uuid4())
        session = ChatSession(session_id=session_id, ip_address=ip_address)
        db.add(session)
        await db.flush()

    # ── Load conversation history ────────────────────────────────────────────
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session.session_id)
        .order_by(ChatMessage.created_at)
    )
    history = result.scalars().all()

    # ── Build system prompt with verified knowledge ──────────────────────────
    system_content = _SYSTEM_PROMPT
    if _STATIC_KNOWLEDGE:
        system_content += (
            "\n\nAZTU KNOWLEDGE BASE (yeganə icazə verilən məlumat mənbəyi):\n"
            f"{_STATIC_KNOWLEDGE}"
        )

    messages = [{"role": "system", "content": system_content}]
    for msg in history:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": message})

    # ── Call OpenAI ──────────────────────────────────────────────────────────
    client = AsyncOpenAI(api_key=settings.OPEN_AI_KEY)
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=400,
        temperature=0.3,
    )
    reply = response.choices[0].message.content or ""

    # ── Persist messages ─────────────────────────────────────────────────────
    db.add(ChatMessage(session_id=session.session_id, role="user", content=message))
    db.add(ChatMessage(session_id=session.session_id, role="assistant", content=reply))
    session.last_active_at = datetime.now(timezone.utc)
    await db.commit()

    return reply, session.session_id
