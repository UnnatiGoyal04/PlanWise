from pydantic import BaseModel

class TaskCreate(BaseModel):
    title:str
    subject:str
    description:str | None=None
    priority:str
    estimated_hours: int | None=None
    completed:bool = False