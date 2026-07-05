from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/",
    response_model=TaskResponse
)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db)
):
    db_task = await task_service.create_task(task, db)
    return db_task
@router.get(
    "/",
    response_model=list[TaskResponse]
)
async def get_tasks(
    db: AsyncSession = Depends(get_db)
):
    tasks = await task_service.get_tasks(db)
    return tasks
@router.get(
    "/{id}",
    response_model=TaskResponse
)    
async def get_task(
    id:int,
    db:AsyncSession=Depends(get_db)
):
    task = await task_service.get_task(id, db)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return task
@router.put(
    "/{id}",
    response_model=TaskResponse
)
async def update_task(
    id: int,
    task: TaskUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated_task = await task_service.update_task(
        id=id,
        task_data=task,
        db=db
    )
    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return updated_task
@router.delete(
    "/{id}"
)
async def delete_task(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    deleted = await task_service.delete_task(
        id=id,
        db=db
    )
    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return {
        "message": "Task deleted successfully"
    }