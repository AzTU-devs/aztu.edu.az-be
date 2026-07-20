"""RBAC service — permission resolution, the six super-admin invariants, role CRUD.

Permissions are resolved from the database on every request, never from JWT claims:
a revoked role must take effect immediately, not after the 15-minute access token
expires. The cost is mitigated by a 30 s TTL cache keyed on ``role_id`` — the user
row itself is always read fresh, so ``is_active`` and ``role_id`` changes are instant.

``super_admin`` is implicit-all: it owns zero ``role_permissions`` rows and is
short-circuited in :func:`has_permission`, so no amount of DB state can neuter it.
"""

import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, FrozenSet, List, Optional, Tuple

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import delete, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.core.permissions import (
    DOMAIN_LABELS,
    DOMAIN_ORDER,
    PERMISSION_KEYS,
    SUPER_ADMIN_CODE,
)
from app.models.admin.admin_user import AdminUser
from app.models.admin.role import Permission, Role, role_permissions

logger = get_logger(__name__)

ROLE_CACHE_TTL_SECONDS = 30.0


class RbacViolation(Exception):
    """An invariant (R1–R6) was violated. Carries the response the client sees."""

    def __init__(self, message: str, status_code: int = status.HTTP_409_CONFLICT, **extra):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.extra = extra

    def response(self) -> JSONResponse:
        content = {"status_code": self.status_code, "message": self.message}
        content.update(self.extra)
        return JSONResponse(content=content, status_code=self.status_code)


@dataclass(frozen=True)
class RoleSnapshot:
    id: int
    code: str
    is_system: bool
    permissions: FrozenSet[str]

    @property
    def is_super_admin(self) -> bool:
        return self.code == SUPER_ADMIN_CODE


_role_cache: Dict[int, Tuple[float, Optional[RoleSnapshot]]] = {}


def invalidate_role_cache(role_id: Optional[int] = None) -> None:
    if role_id is None:
        _role_cache.clear()
    else:
        _role_cache.pop(role_id, None)


async def get_role_snapshot(db: AsyncSession, role_id: Optional[int]) -> Optional[RoleSnapshot]:
    if role_id is None:
        return None

    cached = _role_cache.get(role_id)
    if cached and (time.monotonic() - cached[0]) < ROLE_CACHE_TTL_SECONDS:
        return cached[1]

    role = (await db.execute(select(Role).where(Role.id == role_id))).scalar_one_or_none()
    if role is None:
        _role_cache[role_id] = (time.monotonic(), None)
        return None

    if role.code == SUPER_ADMIN_CODE:
        keys: FrozenSet[str] = frozenset()
    else:
        rows = await db.execute(
            select(Permission.key)
            .join(role_permissions, role_permissions.c.permission_id == Permission.id)
            .where(role_permissions.c.role_id == role_id)
        )
        keys = frozenset(rows.scalars().all())

    snapshot = RoleSnapshot(
        id=role.id, code=role.code, is_system=bool(role.is_system), permissions=keys
    )
    _role_cache[role_id] = (time.monotonic(), snapshot)
    return snapshot


async def get_role_permissions(db: AsyncSession, role_id: Optional[int]) -> FrozenSet[str]:
    snapshot = await get_role_snapshot(db, role_id)
    return snapshot.permissions if snapshot else frozenset()


async def has_permission(db: AsyncSession, user: AdminUser, key: Optional[str]) -> bool:
    snapshot = await get_role_snapshot(db, user.role_id)
    if snapshot is None:
        return False
    if snapshot.is_super_admin:
        return True
    if not key:
        return False
    return key in snapshot.permissions


async def is_super_admin(db: AsyncSession, user: AdminUser) -> bool:
    snapshot = await get_role_snapshot(db, user.role_id)
    return bool(snapshot and snapshot.is_super_admin)


# ── Invariants ─────────────────────────────────────────────────────────────────

def assert_not_self(actor: Optional[AdminUser], target_user_id: Optional[int]) -> None:
    """R5 — no self-lockout. Checked before R4 so the message is the clearer one."""
    if actor is not None and target_user_id is not None and actor.id == target_user_id:
        raise RbacViolation("Öz rolunuzu və ya statusunuzu dəyişə bilməzsiniz.")


async def assert_super_admin_floor(db: AsyncSession, excluding_user_id: Optional[int] = None) -> None:
    """R4 — never zero active super admins.

    Runs inside the caller's transaction and locks the surviving super-admin rows,
    so two concurrent demotions cannot both observe a safe count.
    """
    stmt = (
        select(AdminUser.id)
        .join(Role, Role.id == AdminUser.role_id)
        .where(
            Role.code == SUPER_ADMIN_CODE,
            AdminUser.is_active == True,  # noqa: E712
        )
        .with_for_update(of=AdminUser)
    )
    if excluding_user_id is not None:
        stmt = stmt.where(AdminUser.id != excluding_user_id)

    remaining = len((await db.execute(stmt)).scalars().all())
    if remaining < 1:
        raise RbacViolation("Sistemdə ən azı bir aktiv super admin qalmalıdır.")


async def is_super_admin_user_id(db: AsyncSession, user_id: int) -> bool:
    code = (
        await db.execute(
            select(Role.code).join(AdminUser, AdminUser.role_id == Role.id).where(AdminUser.id == user_id)
        )
    ).scalar_one_or_none()
    return code == SUPER_ADMIN_CODE


async def _role_or_violation(db: AsyncSession, role_id: int) -> Role:
    role = (await db.execute(select(Role).where(Role.id == role_id))).scalar_one_or_none()
    if role is None:
        raise RbacViolation("Rol tapılmadı.", status.HTTP_404_NOT_FOUND)
    return role


async def _user_count_for_role(db: AsyncSession, role_id: int) -> int:
    return (
        await db.execute(
            select(func.count()).select_from(AdminUser).where(AdminUser.role_id == role_id)
        )
    ).scalar_one()


async def _permission_ids(db: AsyncSession, keys: List[str]) -> List[int]:
    if not keys:
        return []
    rows = await db.execute(select(Permission.id).where(Permission.key.in_(keys)))
    return list(rows.scalars().all())


def _validate_keys(keys: List[str]) -> List[str]:
    cleaned = sorted({k.strip() for k in keys if k and k.strip()})
    unknown = sorted(set(cleaned) - PERMISSION_KEYS)
    if unknown:
        raise RbacViolation(
            f"Naməlum icazə açarı: {', '.join(unknown)}", status.HTTP_400_BAD_REQUEST
        )
    return cleaned


# ── Permissions catalogue ──────────────────────────────────────────────────────

async def list_permissions(db: AsyncSession):
    try:
        rows = (await db.execute(select(Permission))).scalars().all()
        by_domain: Dict[str, List[dict]] = {}
        for row in rows:
            by_domain.setdefault(row.domain, []).append(
                {
                    "id": row.id,
                    "key": row.key,
                    "action": row.action,
                    "label_az": row.label_az,
                    "label_en": row.label_en,
                }
            )

        ordered = [d for d in DOMAIN_ORDER if d in by_domain]
        ordered += sorted(d for d in by_domain if d not in DOMAIN_ORDER)

        data = []
        for domain in ordered:
            label_az, label_en = DOMAIN_LABELS.get(domain, (domain, domain))
            data.append(
                {
                    "domain": domain,
                    "label_az": label_az,
                    "label_en": label_en,
                    "permissions": sorted(by_domain[domain], key=lambda p: p["key"]),
                }
            )

        return JSONResponse(content={"status_code": 200, "data": data}, status_code=status.HTTP_200_OK)
    except Exception as exc:
        logger.exception("Failed to list permissions: %s", exc)
        return JSONResponse(
            content={"status_code": 500, "message": "İcazələr yüklənmədi."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ── Roles ──────────────────────────────────────────────────────────────────────

async def list_roles(db: AsyncSession):
    try:
        roles = (await db.execute(select(Role).order_by(Role.is_system.desc(), Role.id))).scalars().all()

        user_counts = dict(
            (
                await db.execute(
                    select(AdminUser.role_id, func.count())
                    .where(AdminUser.role_id.isnot(None))
                    .group_by(AdminUser.role_id)
                )
            ).all()
        )
        grant_counts = dict(
            (
                await db.execute(
                    select(role_permissions.c.role_id, func.count()).group_by(role_permissions.c.role_id)
                )
            ).all()
        )

        data = [
            {
                "id": role.id,
                "code": role.code,
                "name_az": role.name_az,
                "name_en": role.name_en,
                "description": role.description,
                "is_system": bool(role.is_system),
                "user_count": user_counts.get(role.id, 0),
                # null = implicit all
                "permission_count": None if role.code == SUPER_ADMIN_CODE else grant_counts.get(role.id, 0),
            }
            for role in roles
        ]
        return JSONResponse(content={"status_code": 200, "data": data}, status_code=status.HTTP_200_OK)
    except Exception as exc:
        logger.exception("Failed to list roles: %s", exc)
        return JSONResponse(
            content={"status_code": 500, "message": "Rollar yüklənmədi."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def get_role_detail(db: AsyncSession, role_id: int):
    try:
        role = await _role_or_violation(db, role_id)
        keys = (
            []
            if role.code == SUPER_ADMIN_CODE
            else sorted(
                (
                    await db.execute(
                        select(Permission.key)
                        .join(role_permissions, role_permissions.c.permission_id == Permission.id)
                        .where(role_permissions.c.role_id == role_id)
                    )
                ).scalars().all()
            )
        )
        return JSONResponse(
            content={
                "status_code": 200,
                "data": {
                    "id": role.id,
                    "code": role.code,
                    "name_az": role.name_az,
                    "name_en": role.name_en,
                    "description": role.description,
                    "is_system": bool(role.is_system),
                    "user_count": await _user_count_for_role(db, role_id),
                    "permissions": keys,
                },
            },
            status_code=status.HTTP_200_OK,
        )
    except RbacViolation as exc:
        return exc.response()
    except Exception as exc:
        logger.exception("Failed to load role %s: %s", role_id, exc)
        return JSONResponse(
            content={"status_code": 500, "message": "Rol yüklənmədi."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def create_role(db: AsyncSession, payload):
    try:
        code = (payload.code or "").strip().lower()
        if not code:
            raise RbacViolation("Rol kodu boş ola bilməz.", status.HTTP_400_BAD_REQUEST)
        if code == SUPER_ADMIN_CODE:
            raise RbacViolation("Bu rol kodu sistem tərəfindən istifadə olunur.")

        existing = (await db.execute(select(Role.id).where(Role.code == code))).scalar_one_or_none()
        if existing:
            raise RbacViolation("Bu kodla rol artıq mövcuddur.")

        keys = _validate_keys(list(payload.permissions or []))

        role = Role(
            code=code,
            name_az=payload.name_az.strip(),
            name_en=payload.name_en.strip(),
            description=payload.description,
            is_system=False,
            created_at=datetime.now(timezone.utc),
        )
        db.add(role)
        await db.flush()

        permission_ids = await _permission_ids(db, keys)
        if permission_ids:
            await db.execute(
                insert(role_permissions),
                [{"role_id": role.id, "permission_id": pid} for pid in permission_ids],
            )

        await db.commit()
        invalidate_role_cache(role.id)

        return JSONResponse(
            content={"status_code": 201, "message": "Rol yaradıldı.", "data": {"id": role.id}},
            status_code=status.HTTP_201_CREATED,
        )
    except RbacViolation as exc:
        await db.rollback()
        return exc.response()
    except Exception as exc:
        await db.rollback()
        logger.exception("Failed to create role: %s", exc)
        return JSONResponse(
            content={"status_code": 500, "message": "Rol yaradılmadı."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_role(db: AsyncSession, role_id: int, payload):
    try:
        role = await _role_or_violation(db, role_id)

        if payload.name_az is not None:
            role.name_az = payload.name_az.strip()
        if payload.name_en is not None:
            role.name_en = payload.name_en.strip()
        role.description = payload.description
        role.updated_at = datetime.now(timezone.utc)

        await db.commit()
        invalidate_role_cache(role_id)

        return JSONResponse(
            content={"status_code": 200, "message": "Rol yeniləndi."}, status_code=status.HTTP_200_OK
        )
    except RbacViolation as exc:
        await db.rollback()
        return exc.response()
    except Exception as exc:
        await db.rollback()
        logger.exception("Failed to update role %s: %s", role_id, exc)
        return JSONResponse(
            content={"status_code": 500, "message": "Rol yenilənmədi."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_role_permissions(db: AsyncSession, role_id: int, payload):
    """R2 — super_admin's grant set is not editable; it has none by design."""
    try:
        role = await _role_or_violation(db, role_id)
        if role.code == SUPER_ADMIN_CODE:
            raise RbacViolation("Super admin rolunun icazələri dəyişdirilə bilməz.")

        keys = _validate_keys(list(payload.permissions or []))
        permission_ids = await _permission_ids(db, keys)

        await db.execute(delete(role_permissions).where(role_permissions.c.role_id == role_id))
        if permission_ids:
            await db.execute(
                insert(role_permissions),
                [{"role_id": role_id, "permission_id": pid} for pid in permission_ids],
            )
        role.updated_at = datetime.now(timezone.utc)

        await db.commit()
        invalidate_role_cache(role_id)

        return JSONResponse(
            content={"status_code": 200, "message": "Rolun icazələri yeniləndi."},
            status_code=status.HTTP_200_OK,
        )
    except RbacViolation as exc:
        await db.rollback()
        return exc.response()
    except Exception as exc:
        await db.rollback()
        logger.exception("Failed to update permissions of role %s: %s", role_id, exc)
        return JSONResponse(
            content={"status_code": 500, "message": "Rolun icazələri yenilənmədi."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_role(db: AsyncSession, role_id: int, reassign_to_role_id: Optional[int] = None):
    """R1 — system roles are undeletable. R6 — attached users must be reassigned."""
    try:
        role = await _role_or_violation(db, role_id)
        if role.is_system:
            raise RbacViolation("Sistem rolunu silmək olmaz.")

        attached = (
            (
                await db.execute(
                    select(AdminUser.username).where(AdminUser.role_id == role_id).order_by(AdminUser.username)
                )
            )
            .scalars()
            .all()
        )

        if attached:
            if reassign_to_role_id is None:
                raise RbacViolation(
                    "Bu rola bağlı istifadəçilər var: "
                    + ", ".join(attached)
                    + ". Silməzdən əvvəl başqa rol təyin edin."
                )
            if reassign_to_role_id == role_id:
                raise RbacViolation("Silinən rol yeni rol kimi təyin edilə bilməz.", status.HTTP_400_BAD_REQUEST)

            target = (
                await db.execute(select(Role.id).where(Role.id == reassign_to_role_id))
            ).scalar_one_or_none()
            if target is None:
                raise RbacViolation("Təyin ediləcək rol tapılmadı.", status.HTTP_404_NOT_FOUND)

            for user in (
                (await db.execute(select(AdminUser).where(AdminUser.role_id == role_id))).scalars().all()
            ):
                user.role_id = reassign_to_role_id
                user.updated_at = datetime.now(timezone.utc)
            await db.flush()

            await assert_super_admin_floor(db)

        await db.execute(delete(role_permissions).where(role_permissions.c.role_id == role_id))
        await db.delete(role)
        await db.commit()
        invalidate_role_cache()

        return JSONResponse(
            content={"status_code": 200, "message": "Rol silindi."}, status_code=status.HTTP_200_OK
        )
    except RbacViolation as exc:
        await db.rollback()
        return exc.response()
    except Exception as exc:
        await db.rollback()
        logger.exception("Failed to delete role %s: %s", role_id, exc)
        return JSONResponse(
            content={"status_code": 500, "message": "Rol silinmədi."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
