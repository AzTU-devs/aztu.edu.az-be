from app.core.session import get_db
from app.api.v1.schema.project import *
from app.services.news_category import *
from app.utils.language import get_language
from app.api.v1.schema.announcement import *
from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.get("/all")
async def get_news_categories_endpoint(
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    return await get_news_categories(
        lang_code=lang_code,
        db=db
    )

@router.post("/create")
async def create_new_category_endpoint(
    az_title: str = Form(...),
    en_title: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    return await create_news_category(
        az_title=az_title,
        en_title=en_title,
        db=db
    )