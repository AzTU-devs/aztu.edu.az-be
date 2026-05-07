from typing import Optional

from fastapi import APIRouter, Depends, Query, Request

from app.core.elasticsearch import get_es
from app.core.rate_limit import limiter
from app.utils.language import get_language
from app.services.search import search as search_service, DOC_TYPES

router = APIRouter()


@router.get("")
@limiter.limit("30/minute")
async def search_endpoint(
    request: Request,
    q: str = Query(..., min_length=1, max_length=200, description="Search query"),
    types: Optional[str] = Query(
        None,
        description="Comma-separated subset of: " + ",".join(DOC_TYPES),
    ),
    limit: int = Query(8, ge=1, le=20, description="Hits per type"),
    lang_code: str = Depends(get_language),
):
    requested_types = None
    if types:
        requested_types = [t.strip() for t in types.split(",") if t.strip()]

    es = await get_es()
    payload = await search_service(
        es=es,
        query=q,
        lang=lang_code,
        types=requested_types,
        limit=limit,
    )
    return {
        "status_code": 200,
        "query": q,
        "lang": lang_code,
        "results": payload["results"],
        "total": payload["total"],
        "degraded": payload["degraded"],
    }
