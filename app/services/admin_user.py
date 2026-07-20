"""Admin-user CRUD.

Every mutation that could reduce the set of active super admins runs
``assert_super_admin_floor`` (R4) *after* the change is flushed but *before* the
commit, so the guard reads the post-mutation state inside the same transaction and
a concurrent demotion cannot slip past it. R5 (self-lockout) is checked first —
its message is the more useful one when both apply.
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.core.security import hash_password
from app.models.admin.admin_user import AdminUser
from app.models.admin.role import Role
from app.services.rbac import RbacViolation, assert_not_self, assert_super_admin_floor

logger = get_logger(__name__)

MAX_PAGE_SIZE = 100


def _role_payload(role: Optional[Role]) -> Optional[dict]:
    if role is None:
        return None
    return {
        "id": role.id,
        "code": role.code,
        "name_az": role.name_az,
        "name_en": role.name_en,
        "is_system": bool(role.is_system),
    }


def _user_payload(user: AdminUser, role: Optional[Role]) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "is_active": bool(user.is_active),
        "role": _role_payload(role),
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None,
    }


async def _user_or_violation(db: AsyncSession, user_id: int) -> AdminUser:
    user = (await db.execute(select(AdminUser).where(AdminUser.id == user_id))).scalar_one_or_none()
    if user is None:
        raise RbacViolation("İstifadəçi tapılmadı.", status.HTTP_404_NOT_FOUND)
    return user


def _error(message: str, code: int) -> JSONResponse:
    return JSONResponse(content={"status_code": code, "message": message}, status_code=code)


def _ok(message: str, data: Optional[dict] = None, code: int = status.HTTP_200_OK) -> JSONResponse:
    content = {"status_code": code, "message": message}
    if data is not None:
        content["data"] = data
    return JSONResponse(content=content, status_code=code)


async def list_admin_users(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 25,
    q: Optional[str] = None,
    role_id: Optional[int] = None,
    is_active: Optional[bool] = None,
):
    try:
        page = max(1, page)
        page_size = max(1, min(page_size, MAX_PAGE_SIZE))

        filters = []
        if q and q.strip():
            filters.append(AdminUser.username.ilike(f"%{q.strip()}%"))
        if role_id is not None:
            filters.append(AdminUser.role_id == role_id)
        if is_active is not None:
            filters.append(AdminUser.is_active == is_active)

        total = (
            await db.execute(select(func.count()).select_from(AdminUser).where(*filters))
        ).scalar_one()

        rows = (
            await db.execute(
                select(AdminUser, Role)
                .outerjoin(Role, Role.id == AdminUser.role_id)
                .where(*filters)
                .order_by(AdminUser.username)
                .offset((page - 1) * page_size)
                .limit(page_size)
            )
        ).all()

        items = [_user_payload(user, role) for user, role in rows]
        return JSONResponse(
            content={
                "status_code": 200,
                "data": {
                    "items": items,
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "has_more": (page - 1) * page_size + len(items) < total,
                },
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as exc:
        logger.exception("Failed to list admin users: %s", exc)
        return _error("İstifadəçilər yüklənmədi.", status.HTTP_500_INTERNAL_SERVER_ERROR)


async def create_admin_user(db: AsyncSession, payload):
    try:
        username = payload.username.strip()
        existing = (
            await db.execute(select(AdminUser.id).where(func.lower(AdminUser.username) == username.lower()))
        ).scalar_one_or_none()
        if existing:
            raise RbacViolation("Bu istifadəçi adı artıq mövcuddur.")

        if payload.role_id is not None:
            role = (await db.execute(select(Role.id).where(Role.id == payload.role_id))).scalar_one_or_none()
            if role is None:
                raise RbacViolation("Rol tapılmadı.", status.HTTP_404_NOT_FOUND)

        user = AdminUser(
            username=username,
            hashed_password=hash_password(payload.password),
            is_active=True if payload.is_active is None else bool(payload.is_active),
            role_id=payload.role_id,
            created_at=datetime.now(timezone.utc),
        )
        db.add(user)
        await db.commit()

        logger.info("Admin user created: %s", username)
        return _ok("İstifadəçi yaradıldı.", {"id": user.id}, status.HTTP_201_CREATED)
    except RbacViolation as exc:
        await db.rollback()
        return exc.response()
    except Exception as exc:
        await db.rollback()
        logger.exception("Failed to create admin user: %s", exc)
        return _error("İstifadəçi yaradılmadı.", status.HTTP_500_INTERNAL_SERVER_ERROR)


async def update_admin_user(db: AsyncSession, user_id: int, payload, actor: AdminUser):
    try:
        user = await _user_or_violation(db, user_id)

        if payload.is_active is not None and bool(payload.is_active) != bool(user.is_active):
            assert_not_self(actor, user_id)

        if payload.username is not None:
            username = payload.username.strip()
            if username and username != user.username:
                clash = (
                    await db.execute(
                        select(AdminUser.id).where(
                            func.lower(AdminUser.username) == username.lower(),
                            AdminUser.id != user_id,
                        )
                    )
                ).scalar_one_or_none()
                if clash:
                    raise RbacViolation("Bu istifadəçi adı artıq mövcuddur.")
                user.username = username

        if payload.is_active is not None:
            user.is_active = bool(payload.is_active)

        user.updated_at = datetime.now(timezone.utc)
        await db.flush()
        await assert_super_admin_floor(db)
        await db.commit()

        return _ok("İstifadəçi yeniləndi.")
    except RbacViolation as exc:
        await db.rollback()
        return exc.response()
    except Exception as exc:
        await db.rollback()
        logger.exception("Failed to update admin user %s: %s", user_id, exc)
        return _error("İstifadəçi yenilənmədi.", status.HTTP_500_INTERNAL_SERVER_ERROR)


async def assign_role(db: AsyncSession, user_id: int, payload, actor: AdminUser):
    try:
        assert_not_self(actor, user_id)
        user = await _user_or_violation(db, user_id)

        role = (await db.execute(select(Role.id).where(Role.id == payload.role_id))).scalar_one_or_none()
        if role is None:
            raise RbacViolation("Rol tapılmadı.", status.HTTP_404_NOT_FOUND)

        user.role_id = payload.role_id
        user.updated_at = datetime.now(timezone.utc)
        await db.flush()
        await assert_super_admin_floor(db)
        await db.commit()

        logger.info("Role %s assigned to admin user %s by %s", payload.role_id, user.username, actor.username)
        return _ok("İstifadəçinin rolu yeniləndi.")
    except RbacViolation as exc:
        await db.rollback()
        return exc.response()
    except Exception as exc:
        await db.rollback()
        logger.exception("Failed to assign role to admin user %s: %s", user_id, exc)
        return _error("Rol təyin edilmədi.", status.HTTP_500_INTERNAL_SERVER_ERROR)


async def reset_password(db: AsyncSession, user_id: int, payload, actor: AdminUser):
    try:
        user = await _user_or_violation(db, user_id)

        user.hashed_password = hash_password(payload.password)
        # Any live session for this account is no longer trustworthy.
        user.refresh_token_hash = None
        user.updated_at = datetime.now(timezone.utc)
        await db.commit()

        logger.info("Password reset for admin user %s by %s", user.username, actor.username)
        return _ok("Şifrə yeniləndi.")
    except RbacViolation as exc:
        await db.rollback()
        return exc.response()
    except Exception as exc:
        await db.rollback()
        logger.exception("Failed to reset password for admin user %s: %s", user_id, exc)
        return _error("Şifrə yenilənmədi.", status.HTTP_500_INTERNAL_SERVER_ERROR)


async def set_active(db: AsyncSession, user_id: int, active: bool, actor: AdminUser):
    try:
        if not active:
            assert_not_self(actor, user_id)
        user = await _user_or_violation(db, user_id)

        user.is_active = active
        if not active:
            user.refresh_token_hash = None
        user.updated_at = datetime.now(timezone.utc)
        await db.flush()
        await assert_super_admin_floor(db)
        await db.commit()

        return _ok("İstifadəçi aktivləşdirildi." if active else "İstifadəçi deaktiv edildi.")
    except RbacViolation as exc:
        await db.rollback()
        return exc.response()
    except Exception as exc:
        await db.rollback()
        logger.exception("Failed to change active state of admin user %s: %s", user_id, exc)
        return _error("İstifadəçinin statusu dəyişdirilmədi.", status.HTTP_500_INTERNAL_SERVER_ERROR)


async def delete_admin_user(db: AsyncSession, user_id: int, actor: AdminUser):
    try:
        assert_not_self(actor, user_id)
        user = await _user_or_violation(db, user_id)

        username = user.username
        await db.delete(user)
        await db.flush()
        await assert_super_admin_floor(db)
        await db.commit()

        logger.info("Admin user %s deleted by %s", username, actor.username)
        return _ok("İstifadəçi silindi.")
    except RbacViolation as exc:
        await db.rollback()
        return exc.response()
    except Exception as exc:
        await db.rollback()
        logger.exception("Failed to delete admin user %s: %s", user_id, exc)
        return _error("İstifadəçi silinmədi.", status.HTTP_500_INTERNAL_SERVER_ERROR)
