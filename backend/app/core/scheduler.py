from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.background.cleanup import run_cleanup_job


scheduler = AsyncIOScheduler()


def add_scheduler_jobs():
    scheduler.add_job(
        run_cleanup_job,
        "interval",
        minutes=1,
    )