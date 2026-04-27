import time
from playwright.async_api import async_playwright
from fastapi import APIRouter
from app.core.logger import get_logger

logger = get_logger("aztu.article")

SCOPUS_URL = "https://www.scopus.com/pages/organization/60071968"
WEB_OF_SCIENCE_URL = "https://www.webofscience.com/wos/woscc/summary/5667f913-5f6b-4e0b-8fe9-e12d8f6be1f1-01af1662f4/relevance/1?state=%7B%22searchType%22:%22generalSearch%22%7D"

SCOPUS_COUNTER_PATH = "/html/body/div[1]/div/main/div/section/div/div/div[1]/div/header/div/section/div/div[1]/div/div/div/div[1]/a/span/span"
WEB_OF_SCIENCE_COUNTER_PATH = "/html/body/app-wos/main/div/div[1]/div/div/div[2]/app-input-route/app-base-summary-component/app-search-friendly-display/div[1]/app-general-search-friendly-display/div/div/h1/span"


async def fetch_article_counters() -> dict:
    logger.info("article counters scrape started")
    start = time.monotonic()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
        )
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            locale="en-US",
        )
        page = await context.new_page()

        scopus_count = None
        try:
            await page.goto(SCOPUS_URL, wait_until="load", timeout=30000)
            try:
                await page.wait_for_load_state("networkidle", timeout=10000)
            except Exception:
                pass
            logger.debug("scopus landed on: %s | title: %s", page.url, await page.title())
            # accept cookie / GDPR consent if present
            for selector in ["button#onetrust-accept-btn-handler", "button:has-text('Accept')", "button:has-text('Accept all')"]:
                try:
                    btn = await page.query_selector(selector)
                    if btn:
                        await btn.click()
                        await page.wait_for_load_state("networkidle", timeout=8000)
                        break
                except Exception:
                    pass
            el = await page.wait_for_selector("[data-testid='clickable-count']", timeout=15000)
            scopus_count = (await el.inner_text()).strip()
            logger.info("scopus counter fetched: %s", scopus_count)
        except Exception as exc:
            logger.error("scopus scrape failed: %s", exc)

        wos_count = None
        try:
            await page.goto(WEB_OF_SCIENCE_URL, wait_until="load", timeout=30000)
            try:
                await page.wait_for_load_state("networkidle", timeout=15000)
            except Exception:
                pass
            logger.debug("wos landed on: %s | title: %s", page.url, await page.title())
            el = await page.wait_for_selector(".tab-results-count", timeout=20000)
            wos_count = (await el.inner_text()).strip()
            logger.info("wos counter fetched: %s", wos_count)
        except Exception as exc:
            logger.error("wos scrape failed: %s", exc)

        await context.close()
        await browser.close()

    elapsed_ms = (time.monotonic() - start) * 1000
    logger.info("article counters scrape finished in %.1fms — scopus=%s wos=%s", elapsed_ms, scopus_count, wos_count)
    return {"scopus": scopus_count, "wos": wos_count}


router = APIRouter()


@router.get("/counters")
async def get_article_counters():
    logger.debug("GET /api/article/counters requested")
    data = await fetch_article_counters()
    return {"status_code": 200, "data": data}
