from datetime import datetime
import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

# Import scraper job
from src.data.scraper import setup_db, scrape_and_store


def _scrape_job():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] (APScheduler) Starting daily Jumia scrape...")
    try:
        setup_db()
        scrape_and_store()
    except Exception as exc:
        print(f"[{now}] (APScheduler) Error during scrape: {exc}")
    finally:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] (APScheduler) Finished daily Jumia scrape.")


def create_scheduler() -> BackgroundScheduler:
    tz = os.getenv("SCHEDULER_TIMEZONE")  # optional, e.g., "Africa/Lagos" or "UTC"
    scheduler = BackgroundScheduler(timezone=tz) if tz else BackgroundScheduler()

    # Daily at 08:00 local time by default
    hour = int(os.getenv("SCRAPE_HOUR", "8"))
    minute = int(os.getenv("SCRAPE_MINUTE", "0"))
    trigger = CronTrigger(hour=hour, minute=minute)

    scheduler.add_job(
        _scrape_job,
        trigger=trigger,
        id="daily_jumia_scrape",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
        misfire_grace_time=3600,  # 1 hour grace
    )
    return scheduler


def start_scheduler(app) -> None:
    enabled = os.getenv("SCHEDULER_ENABLED", "true").lower() in {"1", "true", "yes", "on"}
    if not enabled:
        print("APScheduler disabled via SCHEDULER_ENABLED env var.")
        return
    scheduler = create_scheduler()
    scheduler.start()
    app.state.scheduler = scheduler
    print("APScheduler started. Daily scrape scheduled at 08:00 (configurable via SCRAPE_HOUR/SCRAPE_MINUTE).")


def shutdown_scheduler(app) -> None:
    scheduler: BackgroundScheduler | None = getattr(app.state, "scheduler", None)
    if scheduler:
        scheduler.shutdown(wait=False)
        print("APScheduler stopped.")