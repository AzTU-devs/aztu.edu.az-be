from fastapi import UploadFile
from app.core.session import get_db
from app.api.v1.schema.news import *
from app.services.menu_category import *
from app.utils.language import get_language
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, File, Form, Query

router = APIRouter()

@router.get("/all")
async def get_menu_categories_endpoint(
    db: AsyncSession = Depends(get_db)
):
    return await get_menu_categories(
        db=db
    )

@router.post("/create")
async def create_menu_category_endpoint(
    title: str,
    db: AsyncSession = Depends(get_db)
):
    return await create_menu_category(
        title=title,
        db=db
    )