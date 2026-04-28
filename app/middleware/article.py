import time
import json
import asyncio
import urllib.request
import urllib.parse
from fastapi import APIRouter
from app.core.logger import get_logger

logger = get_logger("aztu.article")

SCOPUS_SEARCH_URL = "https://api.elsevier.com/content/search/scopus"
SCOPUS_API_KEY = "833d8114bee9d1f779195cd3993b77e4"
SCOPUS_QUERY = (
    'AF-ID(60071968) OR AFFIL("Azerbaijan Technical University") '
    'OR AFFIL("Azərbaycan Texniki Universiteti")'
)

# WEB_OF_SCIENCE_URL = "https://www.webofscience.com/wos/woscc/summary/..."
# WEB_OF_SCIENCE_COUNTER_PATH = "/html/body/app-wos/main/..."


def _fetch_scopus_sync() -> str:
    params = urllib.parse.urlencode({"query": SCOPUS_QUERY, "count": "0"})
    req = urllib.request.Request(
        f"{SCOPUS_SEARCH_URL}?{params}",
        headers={
            "Accept": "application/json",
            "X-ELS-APIKey": SCOPUS_API_KEY,
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    return data["search-results"]["opensearch:totalResults"]


async def fetch_article_counters() -> dict:
    logger.info("article counters fetch started")
    start = time.monotonic()

    scopus_count = None
    try:
        scopus_count = await asyncio.to_thread(_fetch_scopus_sync)
        logger.info("scopus total results: %s", scopus_count)
    except Exception as exc:
        logger.error("scopus fetch failed: %s", exc)

    # wos_count = None
    # WoS requires institutional auth — commented until resolved

    elapsed_ms = (time.monotonic() - start) * 1000
    logger.info("article counters fetch finished in %.1fms", elapsed_ms)
    return {"scopus": scopus_count, "wos": None}


router = APIRouter()


@router.get("/counters")
async def get_article_counters():
    logger.debug("GET /api/article/counters requested")
    data = await fetch_article_counters()
    return {"status_code": 200, "data": data}
