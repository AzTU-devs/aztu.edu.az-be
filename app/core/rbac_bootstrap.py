"""Boot-time RBAC sync — makes an existing production database self-bootstrapping.

Runs in the lifespan before ``verify_permission_map()`` and ``seed_admin_user()``:

1. Upsert the code catalogue into ``permissions``. Rows are never deleted — a key
   that disappeared from the catalogue is reported at WARNING so a stale grant is
   visible rather than silently dropped.
2. Upsert the system roles. ``super_admin`` gets no grant rows (implicit-all); the
   other system roles are refreshed to match code on every boot. Custom roles are
   never touched.
3. Backfill role-less admins — one-shot, self-disabling: it fires only on the first
   boot after the migration, when nobody has a role at all. Pre-existing admins are
   promoted to ``super_admin`` because ``require_admin`` was already binary, so this
   is a no-op in effective privilege and cannot lock anyone out at deploy time.
"""

from datetime import datetime, timezone

from sqlalchemy import func, select, text
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.core.logger import get_logger
from app.core.permissions import PERMISSION_CATALOGUE, SUPER_ADMIN_CODE, SYSTEM_ROLES
from app.models.admin.admin_user import AdminUser
from app.models.admin.role import Permission, Role, role_permissions
from app.services.rbac import invalidate_role_cache

logger = get_logger("aztu.rbac")

VIEWER_ROLE_CODE = "viewer"


async def _sync_permissions(db) -> None:
    now = datetime.now(timezone.utc)
    rows = [
        {
            "key": p.key,
            "domain": p.domain,
            "action": p.action,
            "label_az": p.label_az,
            "label_en": p.label_en,
            "created_at": now,
        }
        for p in PERMISSION_CATALOGUE
    ]
    stmt = pg_insert(Permission).values(rows)
    stmt = stmt.on_conflict_do_update(
        index_elements=[Permission.key],
        set_={
            "domain": stmt.excluded.domain,
            "action": stmt.excluded.action,
            "label_az": stmt.excluded.label_az,
            "label_en": stmt.excluded.label_en,
        },
    )
    await db.execute(stmt)

    catalogue_keys = {p.key for p in PERMISSION_CATALOGUE}
    stored = set((await db.execute(select(Permission.key))).scalars().all())
    orphaned = sorted(stored - catalogue_keys)
    if orphaned:
        logger.warning(
            "permissions rows with no catalogue entry (grants on them still resolve to nothing): %s",
            ", ".join(orphaned),
        )


async def _sync_system_roles(db) -> None:
    now = datetime.now(timezone.utc)
    permission_ids = dict(
        (await db.execute(select(Permission.key, Permission.id))).all()
    )

    for definition in SYSTEM_ROLES:
        role = (
            await db.execute(select(Role).where(Role.code == definition.code))
        ).scalar_one_or_none()

        if role is None:
            role = Role(
                code=definition.code,
                name_az=definition.name_az,
                name_en=definition.name_en,
                description=definition.description_az,
                is_system=True,
                created_at=now,
            )
            db.add(role)
            await db.flush()
            logger.info("Created system role %s", definition.code)
        elif not role.is_system:
            role.is_system = True
            role.updated_at = now

        if definition.implicit_all:
            # super_admin is short-circuited in code; grant rows would be a lie.
            await db.execute(
                role_permissions.delete().where(role_permissions.c.role_id == role.id)
            )
            continue

        wanted = {permission_ids[k] for k in definition.permissions if k in permission_ids}
        current = set(
            (
                await db.execute(
                    select(role_permissions.c.permission_id).where(
                        role_permissions.c.role_id == role.id
                    )
                )
            )
            .scalars()
            .all()
        )

        to_add = wanted - current
        to_drop = current - wanted
        if to_drop:
            await db.execute(
                role_permissions.delete().where(
                    role_permissions.c.role_id == role.id,
                    role_permissions.c.permission_id.in_(to_drop),
                )
            )
        if to_add:
            await db.execute(
                role_permissions.insert(),
                [{"role_id": role.id, "permission_id": pid} for pid in sorted(to_add)],
            )
        if to_add or to_drop:
            logger.info(
                "System role %s grants refreshed (+%d/-%d)", definition.code, len(to_add), len(to_drop)
            )


async def _backfill_roles(db) -> None:
    assigned = (
        await db.execute(
            select(func.count()).select_from(AdminUser).where(AdminUser.role_id.isnot(None))
        )
    ).scalar_one()
    if assigned:
        return

    roleless = (
        await db.execute(
            select(func.count()).select_from(AdminUser).where(AdminUser.role_id.is_(None))
        )
    ).scalar_one()
    if not roleless:
        return

    super_id = (
        await db.execute(select(Role.id).where(Role.code == SUPER_ADMIN_CODE))
    ).scalar_one()

    chosen = (settings.RBAC_BOOTSTRAP_SUPERADMIN or "").strip()
    if chosen:
        target = (
            await db.execute(select(AdminUser).where(AdminUser.username == chosen))
        ).scalar_one_or_none()
        if target is None:
            logger.error(
                "RBAC_BOOTSTRAP_SUPERADMIN=%r does not match any admin user — "
                "falling back to promoting every role-less admin.",
                chosen,
            )
        else:
            viewer_id = (
                await db.execute(select(Role.id).where(Role.code == VIEWER_ROLE_CODE))
            ).scalar_one_or_none()
            target.role_id = super_id
            await db.flush()
            if viewer_id is not None:
                await db.execute(
                    text(
                        "update admin_users set role_id = :viewer_id where role_id is null"
                    ),
                    {"viewer_id": viewer_id},
                )
            logger.warning(
                "RBAC bootstrap: %s promoted to super_admin, all other role-less admins set to viewer.",
                chosen,
            )
            return

    await db.execute(
        text("update admin_users set role_id = :super_id where role_id is null"),
        {"super_id": super_id},
    )
    logger.warning(
        "RBAC bootstrap: %d pre-existing admin user(s) promoted to super_admin "
        "(no-op in effective privilege — require_admin was already binary).",
        roleless,
    )


async def sync_rbac() -> None:
    async with AsyncSessionLocal() as db:
        try:
            await _sync_permissions(db)
            await _sync_system_roles(db)
            await _backfill_roles(db)
            await db.commit()
        except Exception as exc:
            await db.rollback()
            logger.exception("RBAC sync failed: %s", exc)
            raise

    invalidate_role_cache()
    logger.info("RBAC sync complete: %d permissions, %d system roles.", len(PERMISSION_CATALOGUE), len(SYSTEM_ROLES))
