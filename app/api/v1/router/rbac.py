from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schema.rbac import RoleCreate, RolePermissionsUpdate, RoleUpdate
from app.core.auth_dependency import require_admin
from app.core.session import get_db
from app.models.admin.admin_user import AdminUser
from app.services.rbac import (
    create_role,
    delete_role,
    get_role_detail,
    list_permissions,
    list_roles,
    update_role,
    update_role_permissions,
)

router = APIRouter()


@router.get("/permissions")
async def get_permissions_endpoint(
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await list_permissions(db=db)


@router.get("/roles")
async def get_roles_endpoint(
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await list_roles(db=db)


@router.get("/roles/{role_id}")
async def get_role_endpoint(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_role_detail(db=db, role_id=role_id)


@router.post("/roles")
async def create_role_endpoint(
    body: RoleCreate,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_role(db=db, payload=body)


@router.put("/roles/{role_id}")
async def update_role_endpoint(
    role_id: int,
    body: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_role(db=db, role_id=role_id, payload=body)


@router.put("/roles/{role_id}/permissions")
async def update_role_permissions_endpoint(
    role_id: int,
    body: RolePermissionsUpdate,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_role_permissions(db=db, role_id=role_id, payload=body)


@router.delete("/roles/{role_id}")
async def delete_role_endpoint(
    role_id: int,
    reassign_to_role_id: Optional[int] = Query(default=None),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_role(db=db, role_id=role_id, reassign_to_role_id=reassign_to_role_id)
