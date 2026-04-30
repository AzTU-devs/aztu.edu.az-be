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
from app.services.chatbot_scraper import load_knowledge_context

_SYSTEM_PROMPT = """You are the official AI assistant of Azerbaijan Technical University (AzTU).
Your sole purpose is to provide information about AzTU (admissions, faculties,
academic programs, campus life, administration, and university news).

STRICT OPERATING RULES:
1. ONLY answer questions directly related to Azerbaijan Technical University.
2. For ANY question outside this scope, politely refuse by saying:
   "I am designed to assist only with questions regarding Azerbaijan Technical University."
3. CONTENT SAFETY: Do not respond to profanity, insults, hate speech, or offensive language.
   If the user uses such language, state that you cannot assist with requests of that nature.
4. Do not engage in casual conversation or answer non-university related prompts.
5. MAXIMUM response length: 500 characters. Shorter is better.
6. Always respond in the same language the user used (Azerbaijani or English).
7. When VERIFIED AZTU DATA is provided below, ALWAYS prioritize it over your own training data."""

_KB_PATH = Path(__file__).resolve().parents[2] / "aztu_knowledge_base.md"
_STATIC_KNOWLEDGE: str = ""

def _load_static_knowledge() -> str:
    global _STATIC_KNOWLEDGE
    if _STATIC_KNOWLEDGE:
        return _STATIC_KNOWLEDGE
    if _KB_PATH.exists():
        _STATIC_KNOWLEDGE = _KB_PATH.read_text(encoding="utf-8")
    return _STATIC_KNOWLEDGE


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
    knowledge_context = await load_knowledge_context(db)
    static_knowledge = _load_static_knowledge()

    system_content = _SYSTEM_PROMPT
    if static_knowledge:
        system_content += f"\n\nSTATİK BİLİK BAZASI (dəqiq məlumatlar):\n{static_knowledge}"
    if knowledge_context:
        system_content += f"\n\n{knowledge_context}"

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
