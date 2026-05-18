from typing import Optional
from app.core.session import get_db
from app.core.auth_dependency import require_admin
from app.models.admin.admin_user import AdminUser
from app.services.news_category import *
from app.utils.language import get_language
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

@router.get("/{category_id}")
async def get_news_category_details_endpoint(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_news_category_details(category_id=category_id, db=db)

@router.post("/create")
async def create_new_category_endpoint(
    az_title: str = Form(...),
    en_title: str = Form(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_news_category(
        az_title=az_title,
        en_title=en_title,
        db=db
    )


@router.patch("/{category_id}")
async def update_news_category_endpoint(
    category_id: int,
    az_title: Optional[str] = Form(None),
    en_title: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_news_category(
        category_id=category_id,
        az_title=az_title,
        en_title=en_title,
        db=db,
    )


@router.delete("/{category_id}/delete")
async def delete_news_category_endpoint(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_news_category(category_id=category_id, db=db)
