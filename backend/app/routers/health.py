from fastapi import APIRouter, Depends, Request
from app.core.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.services.health_service import check_database
from app.schemas.health import HealthResponse
from app.core.limiter import limiter

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)
@router.get(
    "",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns the current health status of the application.",
)
@limiter.limit("5/minute")
async def health_check(
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    database_connected = await check_database(session)

    return {
        "status": "healthy" if database_connected else "unhealthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "connected" if database_connected else "disconnected",
    }