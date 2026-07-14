from fastapi import APIRouter, Depends, Query, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service
from app.enums.priority import Priority
from app.enums.sort_field import SortField
from app.enums.sort_order import SortOrder
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description=(
        "Creates a new study task for the authenticated user. "
        "The task is automatically associated with the currently logged-in user."
    ),
    response_description="The newly created task.",
)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    db_task = await task_service.create_task(
        task,
        db,
        current_user
    )
    return db_task
@router.get(
    "/",
    response_model=list[TaskResponse],
    summary="Get all tasks",
    description=(
        "Returns the authenticated user's tasks. "
        "Supports filtering, searching, sorting, and pagination."
    ),
    response_description="A list of matching tasks."
)
async def get_tasks(
    priority: Priority | None = Query(
        default=None,
        description="Filter tasks by priority (High, Medium, or Low)."
    ),
    completed: bool | None = Query(
        default=None,
        description="Filter tasks by completion status."
    ),
    search: str | None = Query(
        default=None,
        description="Search tasks by title or description."
    ),
    sort: SortField | None = Query(
        default=None,
        description="Field used to sort the returned tasks."
    ),
    order: SortOrder = Query(
        default=SortOrder.ASC,
        description="Sort order: ascending or descending."
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Page number to retrieve."
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of tasks returned per page."
    ),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    tasks = await task_service.get_tasks(
        priority=priority,
        completed=completed,
        search=search,
        sort=sort,
        order=order,
        page=page,
        limit=limit,
        current_user=current_user,
        db=db
    )    
    return tasks
@router.get(
    "/{id}",
    response_model=TaskResponse
)    
async def get_task(
    id:int,
    current_user: User = Depends(get_current_user),
    db:AsyncSession=Depends(get_db)
):
    return await task_service.get_task(
        id=id,
        current_user=current_user,
        db=db,
    )
@router.put(
    "/{id}",
    response_model=TaskResponse
)
async def update_task(
    id: int,
    task: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await task_service.update_task(
        id=id,
        task_data=task,
        current_user=current_user,
        db=db
    )
@router.delete(
    "/{id}"
)
async def delete_task(
    id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await task_service.delete_task(
        id=id,
        current_user=current_user,
        db=db
    )
    
    return {
        "message": "Task deleted successfully"
    }