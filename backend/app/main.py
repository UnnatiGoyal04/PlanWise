from fastapi import FastAPI
from app.core.settings import settings
from app.routers.home import router as home_router
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)
app.include_router(home_router)
