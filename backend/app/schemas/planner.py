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

    estimated_hours: float = Field(
        description="Estimated hours required to complete the task."
    )

    allocated_hours: float = Field(
        description="Study hours allocated for today's plan."
    )

    score: int = Field(
        description="Calculated planning score."
    )

    reason: str | None = Field(
        default=None,
        description="AI explanation for why this task was scheduled."
    )

class PlannerRecommendation(BaseModel):
    summary: str
    recommendations: list[str]

class PlannerResponse(BaseModel):
    available_hours: float = Field(
        description="Hours available for study."
    )

    allocated_hours: float = Field(
        description="Total allocated study hours."
    )

    tasks: list[PlannedTask]

    recommendation: PlannerRecommendation | None = None

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
                        "estimated_hours": 4,
                        "allocated_hours": 1,
                        "score": 95
                    },
                    {
                        "task_id": 5,
                        "title": "Operating Systems Unit 3",
                        "subject": "Operating Systems",
                        "priority": "Medium",
                        "due_date": "2026-07-27",
                        "estimated_hours": 2,
                        "allocated_hours": 2,
                        "score": 88
                    }
                ]
            }
        }
    )