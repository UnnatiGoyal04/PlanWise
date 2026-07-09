from fastapi import FastAPI

from app.core.settings import settings
from app.routers.home import router as home_router
from app.routers.task import router as task_router
from app.routers.auth import router as auth_router
from app.exception_handlers.handlers import register_exception_handlers
from app.middleware.logging_middleware import register_logging_middleware

from contextlib import asynccontextmanager
from app.database.database import engine
import app.models.task
import app.models.user

@asynccontextmanager
async def lifespan(app):
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,

)
register_exception_handlers(app)
register_logging_middleware(app)

app.include_router(home_router)
app.include_router(task_router)
app.include_router(auth_router)