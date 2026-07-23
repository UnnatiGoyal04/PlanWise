from datetime import date

from pydantic import BaseModel, Field, ConfigDict


class PlannerRequest(BaseModel):
    available_hours: float = Field(
        ...,
        gt=0,
        le=24,
        description="Number of study hours available today."
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "available_hours": 4
            }
        }
    )


class PlannedTask(BaseModel):
    task_id: int = Field(
        description="Unique identifier of the task."
    )

    title: str = Field(
        description="Task title."
    )

    subject: str = Field(
        description="Subject associated with the task."
    )

    priority: str = Field(
        description="Priority assigned to the task."
    )

    due_date: date | None = Field(
        description="Task due date."
    )

    allocated_hours: float = Field(
        description="Hours allocated to this task."
    )

    score: int = Field(
        description="Calculated planning score."
    )


class PlannerResponse(BaseModel):
    available_hours: float = Field(
        description="Hours available for study."
    )

    allocated_hours: float = Field(
        description="Total allocated study hours."
    )

    tasks: list[PlannedTask]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "available_hours": 4,
                "allocated_hours": 4,
                "tasks": [
                    {
                        "task_id": 3,
                        "title": "Graph Algorithms Revision",
                        "subject": "DSA",
                        "priority": "High",
                        "due_date": "2026-07-25",
                        "allocated_hours": 2,
                        "score": 95
                    },
                    {
                        "task_id": 5,
                        "title": "Operating Systems Unit 3",
                        "subject": "Operating Systems",
                        "priority": "Medium",
                        "due_date": "2026-07-27",
                        "allocated_hours": 2,
                        "score": 88
                    }
                ]
            }
        }
    )