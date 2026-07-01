from fastapi import APIRouter
from app.schemas.task import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/",
    response_model=TaskResponse
)
def create_task(task: TaskCreate):
    return TaskResponse(
        id=1,
        title=task.title,
        subject=task.subject,
        description=task.description,
        priority=task.priority,
        estimated_hours=task.estimated_hours,
        completed=task.completed
    )
        
    