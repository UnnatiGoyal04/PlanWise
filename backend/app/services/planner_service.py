from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.planner import (
    PlannerRequest,
    PlannerResponse,
    PlannedTask,
)
from app.services.task_service import get_all_active_tasks
from datetime import date


def calculate_score(task) -> int:
    """
    Calculates a priority score for a task.

    Higher score = higher priority.
    """

    score = 0

    # Priority weight
    if task.priority == "High":
        score += 50
    elif task.priority == "Medium":
        score += 30
    else:
        score += 10

    # Due date weight
    if task.due_date is not None:
        days_left = (task.due_date - date.today()).days

        if days_left <= 0:
            score += 40
        elif days_left <= 1:
            score += 30
        elif days_left <= 7:
            score += 20
        else:
            score += 10

    # Estimated hours weight
    if task.estimated_hours is not None:
        if task.estimated_hours <= 2:
            score += 10
        elif task.estimated_hours <= 5:
            score += 5

    return score


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
                estimated_hours=task.estimated_hours or 0,
                allocated_hours=0,
                score=calculate_score(task),
            )
        )

    planned_tasks.sort(
        key=lambda task: task.score,
        reverse=True,
    )

    remaining_hours = request.available_hours

    for task in planned_tasks:

        if remaining_hours <= 0:
            break

        hours_to_allocate = min(
            task.estimated_hours,
            remaining_hours,
        )

        task.allocated_hours = hours_to_allocate

        remaining_hours -= hours_to_allocate

    allocated_hours = sum(
        task.allocated_hours
        for task in planned_tasks
    )

    return PlannerResponse(
        available_hours=request.available_hours,
        allocated_hours=allocated_hours,
        tasks=planned_tasks,
    )