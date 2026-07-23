from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.routers.home import router as home_router
from app.routers.task import router as task_router
from app.routers.auth import router as auth_router
from app.routers.category import router as category_router
from app.routers.health import router as health_router
from app.routers.planner import router as planner_router

from app.exception_handlers.handlers import register_exception_handlers
from app.middleware.logging_middleware import register_logging_middleware
from app.middleware.request_id_middleware import register_request_id_middleware
from app.core.scheduler import scheduler, add_scheduler_jobs
from app.core.limiter import limiter

from contextlib import asynccontextmanager
from app.database.database import engine
import app.models.task
import app.models.user
import app.models.category

@asynccontextmanager
async def lifespan(app):
    add_scheduler_jobs()
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    contact={
        "name": "Unnati Goyal",
        "email": "unnati4506@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
)
if not settings.TESTING:
    app.state.limiter = limiter
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
register_exception_handlers(app)
register_logging_middleware(app)
register_request_id_middleware(app)

app.include_router(home_router)

app.include_router(
    task_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    auth_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    category_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    health_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    planner_router,
    prefix=settings.API_PREFIX,
)