from pydantic import BaseModel, Field, ConfigDict


class HealthResponse(BaseModel):
    status: str = Field(
        description="Overall health status of the application."
    )

    application: str = Field(
        description="Application name."
    )

    version: str = Field(
        description="Current application version."
    )

    database: str = Field(
        description="Database connectivity status."
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "healthy",
                "application": "PlanWise",
                "version": "1.0.0",
                "database": "connected"
            }
        }
    )