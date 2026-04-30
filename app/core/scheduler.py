from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.logger import get_logger

logger = get_logger("aztu.scheduler")

scheduler = AsyncIOScheduler()


def start_scheduler() -> None:
    from app.services.chatbot_scraper import scrape_all_sources

    # Run on the 1st of every month at 03:00
    scheduler.add_job(
        scrape_all_sources,
        trigger=CronTrigger(day=1, hour=3, minute=0),
        id="monthly_knowledge_scrape",
        replace_existing=True,
        misfire_grace_time=3600,
    )
    scheduler.start()
    logger.info("Scheduler started — knowledge scrape runs on the 1st of each month at 03:00")


def stop_scheduler() -> None:
    scheduler.shutdown(wait=False)
