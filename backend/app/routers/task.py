from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.schemas.task import TaskCreate, TaskResponse
from app.models.task import Task

from sqlalchemy import select

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/",
    response_model=TaskResponse
)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db)
):
    db_task = Task(
        title=task.title,
        subject=task.subject,
        description=task.description,
        priority=task.priority,
        estimated_hours=task.estimated_hours,
        completed=task.completed
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)

    return TaskResponse(
    id=db_task.id,
    title=db_task.title,
    subject=db_task.subject,
    description=db_task.description,
    priority=db_task.priority,
    estimated_hours=db_task.estimated_hours,
    completed=db_task.completed
)
@router.get(
    "/tasks",
    response_model=list[TaskResponse]
)
async def get_tasks(
    db: AsyncSession = Depends(get_db)
):
    query=select(Task)
    result=await db.execute(query)
    tasks= result.scalars().all()
    return tasks
@router.get(
    "/tasks/{id}",
    response_model=TaskResponse
)    
async def get_task(
    id:int,
    db:AsyncSession=Depends(get_db)
):
    query = select(Task).where(Task.id == id)
    result= await db.execute(query)
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return task