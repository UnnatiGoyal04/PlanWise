from datetime import date, datetime

from pydantic import BaseModel, Field, ConfigDict
from app.enums.priority import Priority

class TaskBase(BaseModel):
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
        description="The subject or course associated with this task."
    )

    description: str | None = Field(
        default=None,
        max_length=500,
        description="Optional additional details about the task."
    )

    priority: Priority = Field(
        ...,
        description="Task priority."
    )

    estimated_hours: float | None = Field(
        default=None,
        ge=1,
        le=100,
        description="Estimated number of study hours required."
    )

    completed: bool = Field(
        default=False,
        description="Whether the task has been completed."
    )

    due_date: date | None = Field(
        default=None,
        description="Optional due date for completing the task."
    )

class TaskCreate(TaskBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Revise Binary Trees",
                "subject": "Data Structures",
                "description": "Solve 20 LeetCode problems",
                "priority": "High",
                "estimated_hours": 3,
                "completed": False,
                "due_date": "2026-07-20"
            }
        }
    )

class TaskResponse(BaseModel):
    id: int = Field(
        description="Unique identifier of the task."
    )

    title: str = Field(
        description="Title of the study task."
    )

    subject: str = Field(
        description="The subject or course associated with this task."
    )

    description: str | None = Field(
        description="Additional details about the task."
    )

    priority: Priority = Field(
        description="Priority assigned to the task."
    )

    estimated_hours: float | None = Field(
        description="Estimated number of study hours required."
    )

    completed: bool = Field(
        description="Whether the task has been completed."
    )

    due_date: date | None = Field(
        description="Due date for completing the task."
    )

    created_at: datetime = Field(
        description="Timestamp when the task was created."
    )

    updated_at: datetime = Field(
        description="Timestamp when the task was last updated."
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Revise Binary Trees",
                "subject": "Data Structures",
                "description": "Solve 20 LeetCode problems",
                "priority": "High",
                "estimated_hours": 3,
                "completed": False,
                "due_date": "2026-07-20",
                "created_at": "2026-07-14T10:30:00Z",
                "updated_at": "2026-07-14T10:30:00Z"
            }
        }
    )

class TaskUpdate(TaskBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Revise Binary Trees",
                "subject": "Data Structures",
                "description": "Complete the remaining LeetCode problems",
                "priority": "Medium",
                "estimated_hours": 2,
                "completed": True,
                "due_date": "2026-07-22"
            }
        }
    )