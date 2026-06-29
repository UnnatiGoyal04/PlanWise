from fastapi import FastAPI
from app.routers.home import router as home_router
app = FastAPI(
    title="PlanWise API",
    description="Backend API for the PlanWise AI Study Planner",
    version="0.1.0",
)
app.include_router(home_router)
