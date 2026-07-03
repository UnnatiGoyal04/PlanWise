from fastapi import FastAPI

from app.core.settings import settings
from app.routers.home import router as home_router
from app.routers.task import router as task_router

from contextlib import asynccontextmanager
from app.database.database import create_tables, engine
import app.models.task

@asynccontextmanager
async def lifespan(app):
    await create_tables(engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,

)
app.include_router(home_router)
app.include_router(task_router)