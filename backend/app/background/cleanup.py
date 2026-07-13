from app.database.database import AsyncSessionLocal
from app.services.task_service import cleanup_deleted_tasks as cleanup_service
from app.logging.logger import logger


async def run_cleanup_job():
    logger.info("Cleanup job started.")

    async with AsyncSessionLocal() as db:
        await cleanup_service(db)

    logger.info("Cleanup job finished.")