from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("aztu.scheduler")

scheduler = AsyncIOScheduler()


def start_scheduler() -> None:
    from app.services.chatbot_scraper import scrape_all_sources
    from app.services.activity import purge_expired_activity

    # Run on the 1st of every month at 03:00
    scheduler.add_job(
        scrape_all_sources,
        trigger=CronTrigger(day=1, hour=3, minute=0),
        id="monthly_knowledge_scrape",
        replace_existing=True,
        misfire_grace_time=3600,
    )

    scheduler.add_job(
        purge_expired_activity,
        trigger=CronTrigger(hour=3, minute=30),
        id="activity_log_retention_purge",
        replace_existing=True,
        misfire_grace_time=3600,
    )

    scheduler.start()
    logger.info(
        "Scheduler started — knowledge scrape monthly on the 1st at 03:00, "
        "activity-log purge nightly at 03:30 (retention %d days)",
        settings.AUDIT_LOG_RETENTION_DAYS,
    )


def stop_scheduler() -> None:
    scheduler.shutdown(wait=False)
