from sqlalchemy import select, asc, desc, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.enums.priority import Priority
from app.enums.sort_field import SortField
from app.enums.sort_order import SortOrder
from app.exceptions.task_exceptions import TaskNotFoundException

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
    priority: Priority | None,
    completed: bool | None,
    search: str | None,
    sort: SortField | None,
    order: SortOrder,
    page: int,
    limit: int,
    db: AsyncSession
):
    query = select(Task)

    if priority is not None:
        query = query.where(Task.priority == priority)
    if completed is not None:
        query = query.where(Task.completed == completed)
    if search is not None:
        query = query.where(
            or_(
                Task.title.ilike(f"%{search}%"),
                Task.subject.ilike(f"%{search}%"),
                Task.description.ilike(f"%{search}%")
            )
        )

    sort_column = None
    if sort == SortField.TITLE:
        sort_column = Task.title
    if sort == SortField.PRIORITY:
        sort_column = Task.priority
    if sort == SortField.ESTIMATED_HOURS:
        sort_column = Task.estimated_hours
    if sort_column is not None:
        if order == SortOrder.ASC:
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))

    offset = (page - 1) * limit
    query = query.offset(offset)
    query = query.limit(limit)
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
    if task is None:
        raise TaskNotFoundException()
    return task
async def update_task(
    id: int,
    task_data: TaskUpdate,
    db: AsyncSession
):
    query = select(Task).where(Task.id == id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()
    if task is None:
        raise TaskNotFoundException()
    task.title = task_data.title
    task.subject = task_data.subject
    task.description = task_data.description
    task.priority = task_data.priority
    task.estimated_hours = task_data.estimated_hours
    task.completed = task_data.completed    
    await db.commit()
    await db.refresh(task)
    return task
async def delete_task(
    id: int,
    db: AsyncSession
):
    query = select(Task).where(Task.id == id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()
    if task is None:
        raise TaskNotFoundException()
    await db.delete(task)
    await db.commit()
    return True