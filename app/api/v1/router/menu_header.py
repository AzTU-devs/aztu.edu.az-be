from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.core.auth_dependency import require_admin
from app.utils.language import get_language
from app.utils.file_upload import save_upload, ALLOWED_IMAGE_MIMES
from app.api.v1.schema.menu import (
    CreateHeaderItem, UpdateHeaderItem,
    CreateHeaderSubItem, UpdateHeaderSubItem,
)
from app.services.menu_header import (
    get_header_menu,
    create_header, update_header, delete_header,
    create_header_item, update_header_item, delete_header_item,
    create_header_sub_item, update_header_sub_item, delete_header_sub_item,
)

router = APIRouter()
admin_router = APIRouter(tags=["Menu Header Admin"], dependencies=[Depends(require_admin)])


# ─────────────────────────────────────────────────────────────
# GET  —  public
# ─────────────────────────────────────────────────────────────

@router.get("/")
async def get_header_menu_endpoint(
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_header_menu(lang_code=lang_code, db=db)


# ─────────────────────────────────────────────────────────────
# CRUD  —  MenuHeader (main title + image)
# ─────────────────────────────────────────────────────────────

@admin_router.post("/")
async def create_header_endpoint(
    title_az: str = Form(...),
    title_en: str = Form(...),
    display_order: int = Form(...),
    has_subitems: bool = Form(True),
    direct_url: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
):
    image_url = None
    if image and image.filename:
        relative_path = await save_upload(image, "menu/headers", ALLOWED_IMAGE_MIMES)
        image_url = f"https://aztu.edu.az/{relative_path}"
    return await create_header(
        image_url=image_url,
        direct_url=direct_url or None,
        has_subitems=has_subitems,
        display_order=display_order,
        title_az=title_az,
        title_en=title_en,
        db=db,
    )


@admin_router.put("/{header_id}")
async def update_header_endpoint(
    header_id: int,
    title_az: Optional[str] = Form(None),
    title_en: Optional[str] = Form(None),
    display_order: Optional[int] = Form(None),
    has_subitems: Optional[bool] = Form(None),
    direct_url: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
):
    image_url = None
    if image and image.filename:
        relative_path = await save_upload(image, "menu/headers", ALLOWED_IMAGE_MIMES)
        image_url = f"https://aztu.edu.az/{relative_path}"
    return await update_header(
        header_id=header_id,
        image_url=image_url,
        direct_url=direct_url,
        has_subitems=has_subitems,
        display_order=display_order,
        is_active=is_active,
        title_az=title_az,
        title_en=title_en,
        db=db,
    )


@admin_router.delete("/{header_id}")
async def delete_header_endpoint(
    header_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_header(header_id=header_id, db=db)


# ─────────────────────────────────────────────────────────────
# CRUD  —  MenuHeaderItem (first-level dropdown)
# ─────────────────────────────────────────────────────────────

@admin_router.post("/item")
async def create_header_item_endpoint(
    request: CreateHeaderItem,
    db: AsyncSession = Depends(get_db),
):
    return await create_header_item(request=request, db=db)


@admin_router.put("/item/{item_id}")
async def update_header_item_endpoint(
    item_id: int,
    request: UpdateHeaderItem,
    db: AsyncSession = Depends(get_db),
):
    return await update_header_item(item_id=item_id, request=request, db=db)


@admin_router.delete("/item/{item_id}")
async def delete_header_item_endpoint(
    item_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_header_item(item_id=item_id, db=db)


# ─────────────────────────────────────────────────────────────
# CRUD  —  MenuHeaderSubItem (second-level leaf)
# ─────────────────────────────────────────────────────────────

@admin_router.post("/sub-item")
async def create_header_sub_item_endpoint(
    request: CreateHeaderSubItem,
    db: AsyncSession = Depends(get_db),
):
    return await create_header_sub_item(request=request, db=db)


@admin_router.put("/sub-item/{sub_item_id}")
async def update_header_sub_item_endpoint(
    sub_item_id: int,
    request: UpdateHeaderSubItem,
    db: AsyncSession = Depends(get_db),
):
    return await update_header_sub_item(sub_item_id=sub_item_id, request=request, db=db)


@admin_router.delete("/sub-item/{sub_item_id}")
async def delete_header_sub_item_endpoint(
    sub_item_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_header_sub_item(sub_item_id=sub_item_id, db=db)


router.include_router(admin_router)
