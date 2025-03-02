from pydantic import BaseModel, UUID4, Field
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Title cannot be empty")
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: UUID4
    title: str
    description: Optional[str]
    completed: bool
