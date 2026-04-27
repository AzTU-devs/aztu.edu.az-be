from playwright.async_api import async_playwright
from fastapi import APIRouter

SCOPUS_URL = "https://www.scopus.com/YOUR_PAGE_HERE"
WEB_OF_SCIENCE_URL = "https://www.webofscience.com/YOUR_PAGE_HERE"

SCOPUS_COUNTER_PATH = "/html/body/div[1]/div/main/div/section/div/div/div[1]/div/header/div/section/div/div[1]/div/div/div/div[1]/a/span/span"
WEB_OF_SCIENCE_COUNTER_PATH = "/html/body/app-wos/main/div/div[1]/div/div/div[2]/app-input-route/app-base-summary-component/app-search-friendly-display/div[4]/div[1]/nav/div[2]/div/div/a[1]/span[2]/span/span[1]"


async def fetch_article_counters() -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        scopus_count = None
        try:
            await page.goto(SCOPUS_URL, wait_until="networkidle", timeout=30000)
            el = await page.query_selector(f"xpath={SCOPUS_COUNTER_PATH}")
            if el:
                scopus_count = (await el.inner_text()).strip()
        except Exception:
            pass

        wos_count = None
        try:
            await page.goto(WEB_OF_SCIENCE_URL, wait_until="networkidle", timeout=30000)
            el = await page.query_selector(f"xpath={WEB_OF_SCIENCE_COUNTER_PATH}")
            if el:
                wos_count = (await el.inner_text()).strip()
        except Exception:
            pass

        await browser.close()
        return {"scopus": scopus_count, "wos": wos_count}


router = APIRouter()


@router.get("/counters")
async def get_article_counters():
    data = await fetch_article_counters()
    return {"status_code": 200, "data": data}
