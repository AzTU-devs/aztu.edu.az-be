from datetime import datetime, timezone

import httpx
from bs4 import BeautifulSoup
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.logger import get_logger
from app.models.chat.chatbot_knowledge_source import ChatbotKnowledgeSource
from app.models.chat.chatbot_knowledge import ChatbotKnowledge

logger = get_logger("aztu.scraper")

_MAX_CHARS_PER_SOURCE = 8000
_HEADERS = {"User-Agent": "AzTU-Bot/1.0 (university knowledge scraper)"}


def _extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "iframe"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)[:_MAX_CHARS_PER_SOURCE]


async def scrape_source(source: ChatbotKnowledgeSource, db: AsyncSession) -> bool:
    try:
        async with httpx.AsyncClient(timeout=30, follow_redirects=True, headers=_HEADERS) as client:
            response = await client.get(source.url)
            response.raise_for_status()
        content = _extract_text(response.text)
    except Exception as exc:
        logger.error("Failed to scrape %s: %s", source.url, exc)
        return False

    result = await db.execute(
        select(ChatbotKnowledge).where(ChatbotKnowledge.source_id == source.id)
    )
    existing = result.scalar_one_or_none()

    now = datetime.now(timezone.utc)
    if existing:
        existing.content = content
        existing.scraped_at = now
        existing.is_active = True
    else:
        db.add(ChatbotKnowledge(source_id=source.id, content=content, scraped_at=now))

    source.last_scraped_at = now
    await db.commit()
    logger.info("Scraped %s (%d chars)", source.url, len(content))
    return True


async def scrape_all_sources() -> None:
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(ChatbotKnowledgeSource).where(ChatbotKnowledgeSource.is_active == True)
        )
        sources = result.scalars().all()
        for source in sources:
            await scrape_source(source, db)


async def load_knowledge_context(db: AsyncSession) -> str:
    result = await db.execute(
        select(ChatbotKnowledge).where(ChatbotKnowledge.is_active == True)
    )
    items = result.scalars().all()
    if not items:
        return ""

    parts = []
    for item in items:
        label = item.source.url if item.source else "AzTU"
        parts.append(f"[Mənbə: {label}]\n{item.content}")

    return "DOĞRULANMIŞ AZTU DATA (aşağıdakı məlumatlar dəqiqdir, öz bilikindən üstün tut):\n\n" + "\n\n---\n\n".join(parts)
