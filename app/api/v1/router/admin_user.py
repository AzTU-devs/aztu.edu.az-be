from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schema.rbac import (
    AdminUserCreate,
    AdminUserPasswordReset,
    AdminUserRoleAssign,
    AdminUserUpdate,
)
from app.core.auth_dependency import require_admin
from app.core.session import get_db
from app.models.admin.admin_user import AdminUser
from app.services.admin_user import (
    assign_role,
    create_admin_user,
    delete_admin_user,
    list_admin_users,
    reset_password,
    set_active,
    update_admin_user,
)

router = APIRouter()


@router.get("")
async def get_admin_users_endpoint(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    q: Optional[str] = Query(default=None),
    role_id: Optional[int] = Query(default=None),
    is_active: Optional[bool] = Query(default=None),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await list_admin_users(
        db=db, page=page, page_size=page_size, q=q, role_id=role_id, is_active=is_active
    )


@router.post("")
async def create_admin_user_endpoint(
    body: AdminUserCreate,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_admin_user(db=db, payload=body)


@router.put("/{user_id}")
async def update_admin_user_endpoint(
    user_id: int,
    body: AdminUserUpdate,
    db: AsyncSession = Depends(get_db),
    actor: AdminUser = Depends(require_admin),
):
    return await update_admin_user(db=db, user_id=user_id, payload=body, actor=actor)


@router.put("/{user_id}/role")
async def assign_admin_user_role_endpoint(
    user_id: int,
    body: AdminUserRoleAssign,
    db: AsyncSession = Depends(get_db),
    actor: AdminUser = Depends(require_admin),
):
    return await assign_role(db=db, user_id=user_id, payload=body, actor=actor)


@router.put("/{user_id}/password")
async def reset_admin_user_password_endpoint(
    user_id: int,
    body: AdminUserPasswordReset,
    db: AsyncSession = Depends(get_db),
    actor: AdminUser = Depends(require_admin),
):
    return await reset_password(db=db, user_id=user_id, payload=body, actor=actor)


@router.post("/{user_id}/activate")
async def activate_admin_user_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    actor: AdminUser = Depends(require_admin),
):
    return await set_active(db=db, user_id=user_id, active=True, actor=actor)


@router.post("/{user_id}/deactivate")
async def deactivate_admin_user_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    actor: AdminUser = Depends(require_admin),
):
    return await set_active(db=db, user_id=user_id, active=False, actor=actor)


@router.delete("/{user_id}")
async def delete_admin_user_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    actor: AdminUser = Depends(require_admin),
):
    return await delete_admin_user(db=db, user_id=user_id, actor=actor)
