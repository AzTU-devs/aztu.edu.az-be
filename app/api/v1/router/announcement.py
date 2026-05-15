from app.core.session import get_db
from app.api.v1.schema.project import *
from app.utils.language import get_language
from app.services.announcement import *
from app.core.auth_dependency import require_admin
from app.models.admin.admin_user import AdminUser
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.schema.announcement import *

router = APIRouter()

# ── Public read ────────────────────────────────────────────────────────────────

@router.get("/public/all")
async def get_announcements_endpoint(
    start: int = Query(0, ge=0),
    end: int = Query(4, gt=0, le=100),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    return await get_announcements_user(start=start, end=end, lang=lang, db=db)

@router.get("/{announcement_id}")
async def get_announcement_details_enpoint(
    announcement_id: int,
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db)
):
    return await get_announcement(announcement_id=announcement_id, lang_code=lang_code, db=db)

# ── Admin endpoints (require JWT) ──────────────────────────────────────────────

@router.get("/admin/all")
async def get_announcements_endpoint_admin(
    start: int = Query(0, ge=0),
    end: int = Query(4, gt=0, le=100),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_announcements_admin(start=start, end=end, lang=lang, db=db)

@router.post("/create")
async def create_announcement_endpoint(
    image: Optional[UploadFile] = File(None),
    az_title: str = Form(...),
    az_html_content: str = Form(...),
    en_title: str = Form(...),
    en_html_content: str = Form(...),
    created_at: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_announcement(image=image, az_title=az_title, az_html_content=az_html_content, en_title=en_title, en_html_content=en_html_content, created_at=created_at, db=db)


@router.patch("/{announcement_id}")
async def update_announcement_endpoint(
    announcement_id: int,
    image: Optional[UploadFile] = File(None),
    az_title: Optional[str] = Form(None),
    az_html_content: Optional[str] = Form(None),
    en_title: Optional[str] = Form(None),
    en_html_content: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_announcement(
        announcement_id=announcement_id,
        image=image,
        az_title=az_title,
        az_html_content=az_html_content,
        en_title=en_title,
        en_html_content=en_html_content,
        db=db,
    )


@router.post("/upload-file")
async def upload_announcement_file_endpoint(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_announcement_attachment(file=file, db=db)


@router.delete("/{announcement_id}/delete")
async def delete_announcement_endpoint(
    announcement_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_announcement(announcement_id=announcement_id, db=db)

@router.post("/activate")
async def activate_announcement_endpoint(
    announcement_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await activate_announcement(announcement_id=announcement_id, db=db)

@router.post("/deactivate")
async def deactivate_announcement_endpoint(
    announcement_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await deactivate_announcement(announcement_id=announcement_id, db=db)

@router.post("/reorder")
async def reorder_announcement_endpoint(
    request: ReOrderAnnouncement,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await reorder_announcement(request=request, db=db)
