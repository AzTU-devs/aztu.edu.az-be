from app.services.hero import *
from app.core.session import get_db
from app.core.auth_dependency import require_admin
from app.models.admin.admin_user import AdminUser
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, File, UploadFile

router = APIRouter()

# ── Public read ────────────────────────────────────────────────────────────────

@router.get("/public")
async def get_hero_public_endpoint(db: AsyncSession = Depends(get_db)):
    return await get_hero(db=db)

# ── Admin endpoints (require JWT) ──────────────────────────────────────────────

@router.get("/admin/all")
async def get_hero_admin_endpoint(
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin)
):
    return await get_admin_hero(db=db)

@router.post("/create")
async def create_hero_endpoint(
    video: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin)
):
    return await create_hero(video=video, db=db)

@router.put("/{hero_id}/update")
async def update_hero_endpoint(
    hero_id: int,
    video: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin)
):
    return await update_hero(hero_id=hero_id, video=video, db=db)

@router.post("/activate")
async def activate_hero_endpoint(
    hero_id: int,
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin)
):
    return await activate_hero(hero_id=hero_id, db=db)

@router.post("/deactivate")
async def deactivate_hero_endpoint(
    hero_id: int,
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin)
):
    return await deactivate_hero(hero_id=hero_id, db=db)

@router.delete("/{hero_id}/delete")
async def delete_hero_endpoint(
    hero_id: int,
    db: AsyncSession = Depends(get_db),
    # _: AdminUser = Depends(require_admin)
):
    return await delete_hero(hero_id=hero_id, db=db)
