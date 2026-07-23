from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.planner import (
    PlannerRequest,
    PlannerResponse,
    PlannedTask,
)
from app.services.task_service import get_all_active_tasks


async def generate_plan(
    request: PlannerRequest,
    current_user: User,
    db: AsyncSession,
) -> PlannerResponse:
    """
    Temporary implementation.

    This will later be replaced with the real
    AI scheduling algorithm.
    """

    tasks = await get_all_active_tasks(
        current_user=current_user,
        db=db,
    )

    planned_tasks = []

    for task in tasks:
        planned_tasks.append(
            PlannedTask(
                task_id=task.id,
                title=task.title,
                subject=task.subject,
                priority=task.priority,
                due_date=task.due_date,
                allocated_hours=task.estimated_hours or 0,
                score=0,
            )
        )

    allocated_hours = sum(
        task.allocated_hours
        for task in planned_tasks
    )

    return PlannerResponse(
        available_hours=request.available_hours,
        allocated_hours=allocated_hours,
        tasks=planned_tasks,
    )