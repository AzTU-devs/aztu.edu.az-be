import logging
from datetime import datetime, timezone
from sqlalchemy import select, func
from app.core.database import AsyncSessionLocal
from app.core.security import hash_password
from app.core.config import settings
from app.models.admin.admin_user import AdminUser

logger = logging.getLogger("aztu.startup")


async def seed_admin_user() -> None:
    """
    On first startup, if admin_users table is empty and seed credentials are
    provided via env vars, create the initial admin user.
    """
    if not settings.ADMIN_SEED_USERNAME or not settings.ADMIN_SEED_PASSWORD:
        if settings.ENVIRONMENT == "production":
            logger.warning(
                "ADMIN_SEED_USERNAME / ADMIN_SEED_PASSWORD not set. "
                "No admin user will be created automatically."
            )
        return

    async with AsyncSessionLocal() as db:
        count_result = await db.execute(select(func.count()).select_from(AdminUser))
        count = count_result.scalar_one()

        if count > 0:
            logger.info("Admin users already exist — skipping seed.")
            return

        admin = AdminUser(
            username=settings.ADMIN_SEED_USERNAME,
            hashed_password=hash_password(settings.ADMIN_SEED_PASSWORD),
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )
        db.add(admin)
        await db.commit()
        logger.info("Seeded initial admin user: %s", settings.ADMIN_SEED_USERNAME)
