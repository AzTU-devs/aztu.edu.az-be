from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.api.v1.schema.chatbot_knowledge import KnowledgeSourceCreate, KnowledgeSourceResponse
from app.models.chat.chatbot_knowledge_source import ChatbotKnowledgeSource
from app.services.chatbot_scraper import scrape_source, scrape_all_sources

router = APIRouter()


@router.post("/sources", response_model=KnowledgeSourceResponse, status_code=201)
async def add_source(
    body: KnowledgeSourceCreate,
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    existing = await db.execute(
        select(ChatbotKnowledgeSource).where(ChatbotKnowledgeSource.url == body.url)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Bu URL artıq mövcuddur")
    source = ChatbotKnowledgeSource(url=body.url, label=body.label)
    db.add(source)
    await db.commit()
    await db.refresh(source)
    return source


@router.get("/sources", response_model=list[KnowledgeSourceResponse])
async def list_sources(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ChatbotKnowledgeSource).order_by(ChatbotKnowledgeSource.id))
    return result.scalars().all()


@router.delete("/sources/{source_id}", status_code=204)
async def delete_source(
    source_id: int,
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    result = await db.execute(
        select(ChatbotKnowledgeSource).where(ChatbotKnowledgeSource.id == source_id)
    )
    source = result.scalar_one_or_none()
    if not source:
        raise HTTPException(status_code=404, detail="Tapılmadı")
    await db.delete(source)
    await db.commit()


@router.post("/sources/{source_id}/scrape")
async def trigger_scrape(
    source_id: int,
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin),
):
    result = await db.execute(
        select(ChatbotKnowledgeSource).where(ChatbotKnowledgeSource.id == source_id)
    )
    source = result.scalar_one_or_none()
    if not source:
        raise HTTPException(status_code=404, detail="Tapılmadı")
    success = await scrape_source(source, db)
    if not success:
        raise HTTPException(status_code=502, detail="Scrape uğursuz oldu, URL-i yoxlayın")
    return {"status": "ok", "url": source.url}


@router.post("/sources/scrape-all")
async def trigger_scrape_all(
    # _: AdminUser = Depends(require_admin),
):
    await scrape_all_sources()
    return {"status": "ok"}
