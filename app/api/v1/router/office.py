from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schema.office import OfficeCreate, PublishOffice, UpdateOffice
from app.core.auth_dependency import require_admin
from app.core.session import get_db
from app.models.admin.admin_user import AdminUser
from app.services.office import (
    create_office,
    delete_office,
    get_office_admin,
    get_office_public,
    get_offices_admin,
    get_offices_public,
    publish_office,
    update_office,
    upload_image,
)
from app.utils.language import get_language

router = APIRouter()


# ── Admin ────────────────────────────────────────────────────────────────────


@router.get("/admin/offices")
async def list_offices_admin(
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_offices_admin(db=db)


@router.post("/admin/offices")
async def create_office_endpoint(
    request: OfficeCreate,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_office(request=request, db=db)


@router.get("/admin/offices/{office_id}")
async def read_office_admin(
    office_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_office_admin(office_id=office_id, db=db)


@router.put("/admin/offices/{office_id}")
async def update_office_endpoint(
    office_id: int,
    request: UpdateOffice,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_office(office_id=office_id, request=request, db=db)


@router.delete("/admin/offices/{office_id}")
async def delete_office_endpoint(
    office_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_office(office_id=office_id, db=db)


@router.put("/admin/offices/{office_id}/publish")
async def publish_office_endpoint(
    office_id: int,
    request: PublishOffice,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await publish_office(office_id=office_id, is_active=request.is_active, db=db)


@router.put("/admin/offices/{office_id}/image")
async def upload_office_image_endpoint(
    office_id: int,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_image(office_id=office_id, file=image, db=db)


# ── Public ───────────────────────────────────────────────────────────────────


@router.get("/public/offices")
async def list_offices_public(
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_offices_public(lang=lang, db=db)


@router.get("/public/offices/{slug}")
async def read_office_public(
    slug: str,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_office_public(slug=slug, lang=lang, db=db)
