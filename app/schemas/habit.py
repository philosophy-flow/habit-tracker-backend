import uuid
from typing import List
from pydantic import BaseModel


class HabitAdd(BaseModel):
    name: str


class HabitResponse(BaseModel):
    habit_id: uuid.UUID
    name: str
    dates_completed: List[str]
