from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth_dependency import require_admin
from app.core.session import get_db
from app.models.admin.admin_user import AdminUser
from app.services.activity import (
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    get_activity_filters,
    list_activity,
)

router = APIRouter()


@router.get("")
async def get_activity_endpoint(
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    admin_user_id: Optional[int] = Query(None),
    domain: Optional[str] = Query(None),
    action_key: Optional[str] = Query(None),
    outcome: Optional[str] = Query(None),
    target_type: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await list_activity(
        db=db,
        page=page,
        page_size=page_size,
        admin_user_id=admin_user_id,
        domain=domain,
        action_key=action_key,
        outcome=outcome,
        target_type=target_type,
        date_from=date_from,
        date_to=date_to,
        q=q,
    )


@router.get("/filters")
async def get_activity_filters_endpoint(
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_activity_filters(db=db)
