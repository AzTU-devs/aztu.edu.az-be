import asyncio
import ipaddress
import socket
from datetime import datetime, timezone
from urllib.parse import urlparse

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
_ALLOWED_SCHEMES = {"http", "https"}


def _extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "iframe"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)[:_MAX_CHARS_PER_SOURCE]


async def _assert_public_url(url: str) -> None:
    """Reject URLs that target private/loopback/link-local/reserved IP space.

    Mitigates SSRF: an attacker could otherwise point the scraper at
    169.254.169.254 (cloud metadata), localhost, or an internal service.
    """
    parsed = urlparse(url)
    if parsed.scheme not in _ALLOWED_SCHEMES:
        raise ValueError(f"Disallowed URL scheme: {parsed.scheme!r}")
    host = parsed.hostname
    if not host:
        raise ValueError("URL is missing a hostname")

    loop = asyncio.get_running_loop()
    addrinfo = await loop.getaddrinfo(host, None, type=socket.SOCK_STREAM)
    seen: set[str] = set()
    for entry in addrinfo:
        ip_str = entry[4][0]
        if ip_str in seen:
            continue
        seen.add(ip_str)
        ip = ipaddress.ip_address(ip_str)
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
            or ip.is_unspecified
        ):
            raise ValueError(f"Refusing to fetch internal address {ip_str} for host {host!r}")


async def scrape_source(source: ChatbotKnowledgeSource, db: AsyncSession) -> bool:
    try:
        await _assert_public_url(source.url)
        async with httpx.AsyncClient(
            timeout=30,
            follow_redirects=True,
            max_redirects=3,
            headers=_HEADERS,
        ) as client:
            response = await client.get(source.url)
            for redirect in response.history:
                await _assert_public_url(str(redirect.headers.get("location") or redirect.url))
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
