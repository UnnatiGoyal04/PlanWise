from fastapi import APIRouter, Depends
from app.core.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.services.health_service import check_database

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)
@router.get(
    "",
    summary="Health check",
    description="Returns the current health status of the application.",
)
async def health_check(
    session: AsyncSession = Depends(get_db),
):
    database_connected = await check_database(session)

    return {
        "status": "healthy" if database_connected else "unhealthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "connected" if database_connected else "disconnected",
    }