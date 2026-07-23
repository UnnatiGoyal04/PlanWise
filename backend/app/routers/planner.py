from fastapi import APIRouter, status, Depends

from app.schemas.planner import (
    PlannerRequest,
    PlannerResponse,
)
from app.services import planner_service
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/planner",
    tags=["AI Planner"],
)


@router.post(
    "/generate",
    response_model=PlannerResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate an AI study plan",
    description=(
        "Generates a personalized study plan "
        "based on the user's available study hours."
    ),
)
async def generate_plan(
    request: PlannerRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await planner_service.generate_plan(
        request=request,
        current_user=current_user,
        db=db,
    )