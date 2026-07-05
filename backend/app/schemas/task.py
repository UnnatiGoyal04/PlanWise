from pydantic import BaseModel, Field
from app.enums.priority import Priority

class TaskCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Title of the study task"
    )

    subject: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Subject name"
    )

    description: str | None = Field(
        default=None,
        max_length=500,
        description="Optional description"
    )

    priority: Priority = Field(
        ...,
        description="Task priority"
    )

    estimated_hours: float | None = Field(
        default=None,
        ge=1,
        le=100,
        description="Estimated study hours"
    )

    completed: bool = False

class TaskResponse(BaseModel):
    id: int
    title: str
    subject: str
    description: str | None
    priority: Priority
    estimated_hours: float | None
    completed: bool

class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    subject: str = Field(
        ...,
        min_length=2,
        max_length=50
    )
    description: str | None = Field(
        default=None,
        max_length=500,
        description="Optional description"
    )    
    priority: Priority = Field(
        ...,
        description="Task priority"
    )
    estimated_hours: float | None = Field(
        default=None,
        ge=1,
        le=100,
        description="Estimated study hours"
    )
    completed: bool = False