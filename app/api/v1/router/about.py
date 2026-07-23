from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schema.about import PublishAboutPage, UpdateAboutPage
from app.core.auth_dependency import require_admin
from app.core.session import get_db
from app.models.admin.admin_user import AdminUser
from app.services.about import (
    get_page_admin,
    get_page_public,
    get_pages_admin,
    publish_page,
    update_page,
)
from app.utils.language import get_language

router = APIRouter()


# ── Admin ──────────────────────────────────────────────────────────────────────


@router.get("/admin/pages")
async def list_pages_admin(
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_pages_admin(db=db)


@router.get("/admin/pages/{page_key}")
async def read_page_admin(
    page_key: str,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_page_admin(page_key=page_key, db=db)


@router.put("/admin/pages/{page_key}")
async def update_page_endpoint(
    page_key: str,
    request: UpdateAboutPage,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_page(page_key=page_key, request=request, db=db)


@router.put("/admin/pages/{page_key}/publish")
async def publish_page_endpoint(
    page_key: str,
    request: PublishAboutPage,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await publish_page(page_key=page_key, is_active=request.is_active, db=db)


# ── Public ─────────────────────────────────────────────────────────────────────


@router.get("/public/pages/{page_key}")
async def read_page_public(
    page_key: str,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_page_public(page_key=page_key, lang=lang, db=db)
