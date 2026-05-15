from typing import Optional, List
from fastapi import UploadFile
from app.services.news import *
from app.core.session import get_db
from app.core.auth_dependency import require_admin
from app.models.admin.admin_user import AdminUser
from app.api.v1.schema.news import *
from app.utils.language import get_language
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, File, Form, Query

router = APIRouter()

# ── Public read endpoints (no auth required) ───────────────────────────────────

@router.get("/public/all")
async def get_news_public_endpoint(
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, le=100, description="End index"),
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    return await get_public_news(category_id=category_id, start=start, end=end, lang_code=lang_code, db=db)

@router.get("/gallery")
async def get_news_gallery_endpoint(
    news_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_news_gallery(news_id=news_id, db=db)

@router.get("/{news_id}")
async def get_news_details_endpoint(
    news_id: int,
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    return await get_news_details(news_id=news_id, lang_code=lang_code, db=db)

# ── Admin endpoints (require JWT) ──────────────────────────────────────────────

@router.get("/admin/all")
async def get_news_admin_endpoint(
    news_data: NewsGetter = Depends(),
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_admin_news(category_id=news_data.category_id, start=news_data.start, end=news_data.end, lang_code=lang_code, db=db)

@router.post("/create")
async def create_news_endpoint(
    az_title: str = Form(...),
    en_title: str = Form(...),
    az_html_content: str = Form(...),
    en_html_content: str = Form(...),
    cover_image: UploadFile = File(...),
    gallery_images: Optional[List[UploadFile]] = File(None),
    category_id: int = Form(...),
    created_at: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_news(az_title=az_title, en_title=en_title, az_html_content=az_html_content, en_html_content=en_html_content, cover_image=cover_image, gallery_images=gallery_images, category_id=category_id, created_at=created_at, db=db)

@router.post("/activate")
async def activate_news_endpoint(
    news_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await activate_news(news_id=news_id, db=db)

@router.post("/deactivate")
async def deactivate_news_endpoint(
    news_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await deactivate_news(news_id=news_id, db=db)

@router.post("/reorder")
async def reorder_news_endpoint(
    request: ReOrderNews,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await reorder_news(request=request, db=db)

@router.patch("/{news_id}")
async def update_news_endpoint(
    news_id: int,
    az_title: Optional[str] = Form(None),
    en_title: Optional[str] = Form(None),
    az_html_content: Optional[str] = Form(None),
    en_html_content: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    is_active: Optional[bool] = Form(None),
    cover_image: Optional[UploadFile] = File(None),
    new_gallery_images: Optional[List[UploadFile]] = File(None),
    removed_image_ids: Optional[str] = Form(None),
    gallery_order: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    import json as _json
    parsed_removed = _json.loads(removed_image_ids) if removed_image_ids else None
    parsed_order = _json.loads(gallery_order) if gallery_order else None
    return await update_news(
        news_id=news_id,
        az_title=az_title,
        en_title=en_title,
        az_html_content=az_html_content,
        en_html_content=en_html_content,
        category_id=category_id,
        is_active=is_active,
        cover_image=cover_image,
        new_gallery_images=new_gallery_images,
        removed_image_ids=parsed_removed,
        gallery_order=parsed_order,
        db=db,
    )


@router.delete("/{news_id}/delete")
async def delete_news_endpoint(
    news_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_news(news_id=news_id, db=db)
