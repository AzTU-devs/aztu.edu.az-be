from fastapi import UploadFile
from app.services.news import *
from app.core.session import get_db
from app.api.v1.schema.news import *
from app.utils.language import get_language
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, File, Form, Query

router = APIRouter()

@router.get("/public/all")
async def get_news_public_endpoint(
    category_id: int,
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    return await get_public_news(
        category_id=category_id,
        start=start,
        end=end,
        lang_code=lang_code,
        db=db
    )

@router.get("/admin/all")
async def get_news_public_endpoint(
    category_id: int,
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    return await get_admin_news(
        category_id=category_id,
        start=start,
        end=end,
        lang_code=lang_code,
        db=db
    )

@router.get("/{news_id}")
async def get_news_details_endpoint(
    news_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_news_details(
        news_id=news_id,
        db=db
    )

@router.get("/gallery")
async def get_news_gallery_endpoint(
    news_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_news_gallery(
        news_id=news_id,
        db=db
    )

@router.post("/create")
async def create_news_endpoint(
    az_title: str = Form(...),
    en_title: str = Form(...),
    az_html_content: str = Form(...),
    en_html_content: str = Form(...),
    cover_image: UploadFile = File(...),
    gallery_images: Optional[List[UploadFile]] = File(None),
    category_id: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    return await create_news(
        az_title=az_title,
        en_title=en_title,
        az_html_content=az_html_content,
        en_html_content=en_html_content,
        cover_image=cover_image,
        gallery_images=gallery_images,
        category_id=category_id,
        db=db
    )

@router.post("/activate")
async def activate_news_endpoint(
    news_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await activate_news(
        news_id=news_id,
        db=db
    )

@router.post("/deactivate")
async def activate_news_endpoint(
    news_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await deactivate_news(
        news_id=news_id,
        db=db
    )

@router.post("/reorder")
async def reorder_news_endpoint(
    request: ReOrderNews,
    db: AsyncSession = Depends(get_db)
):
    return await reorder_news(
        request=request,
        db=db
    )

@router.delete("/{news_id}/delete")
async def delete_news_endpoint(
    news_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await delete_news(
        news_id=news_id,
        db=db
    )