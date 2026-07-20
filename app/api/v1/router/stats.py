from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth_dependency import require_admin
from app.core.session import get_db
from app.models.admin.admin_user import AdminUser
from app.services.dashboard import (
    DEFAULT_ACTIVITY_LIMIT,
    MAX_ACTIVITY_LIMIT,
    get_dashboard_stats,
)

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_stats_endpoint(
    activity_limit: int = Query(DEFAULT_ACTIVITY_LIMIT, ge=1, le=MAX_ACTIVITY_LIMIT),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_dashboard_stats(db=db, activity_limit=activity_limit)
