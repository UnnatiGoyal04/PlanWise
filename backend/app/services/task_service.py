from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate

async def create_task(
    task: TaskCreate,
    db: AsyncSession
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
    return db_task
async def get_tasks(
    db: AsyncSession
):
    query = select(Task)
    result = await db.execute(query)
    tasks = result.scalars().all()
    return tasks
async def get_task(
    id: int,
    db: AsyncSession
):
    query = select(Task).where(Task.id == id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()
    return task