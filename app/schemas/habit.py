import uuid
from typing import List, Optional
from datetime import date
from pydantic import BaseModel


class HabitAdd(BaseModel):
    name: str


class HabitCompletion(BaseModel):
    date_completed: date


class HabitResponse(BaseModel):
    habit_id: uuid.UUID
    name: str
    dates_completed: List[HabitCompletion]


class HabitResponseFlat(BaseModel):
    habit_id: uuid.UUID
    name: str
    dates_completed: List[date]


class HabitUpdate(BaseModel):
    name: Optional[str] = None
