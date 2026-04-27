import time
import json
import asyncio
import urllib.request
from fastapi import APIRouter
from app.core.logger import get_logger

logger = get_logger("aztu.article")

SCOPUS_API_URL = "https://www.scopus.com/gateway/organisation-profile-api/organizations/60071968"

# WEB_OF_SCIENCE_URL = "https://www.webofscience.com/wos/woscc/summary/..."
# WEB_OF_SCIENCE_COUNTER_PATH = "/html/body/app-wos/main/..."


def _fetch_scopus_sync() -> dict:
    req = urllib.request.Request(
        SCOPUS_API_URL,
        headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


async def fetch_article_counters() -> dict:
    logger.info("article counters fetch started")
    start = time.monotonic()

    scopus_count = None
    try:
        data = await asyncio.to_thread(_fetch_scopus_sync)
        scopus_count = str(data["metrics"]["documentsCount"])
        logger.info("scopus documents count: %s", scopus_count)
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
