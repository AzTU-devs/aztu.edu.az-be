from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.rate_limit import limiter
from app.core.session import get_db
from app.api.v1.schema.analytics import VisitTrackRequest
from app.services.analytics import record_visit

router = APIRouter()


@router.post("/track")
@limiter.limit("60/minute")
async def track_visit(
    request: Request,
    response: Response,
    body: VisitTrackRequest,
    db: AsyncSession = Depends(get_db),
):
    return await record_visit(request, body.path, db)
