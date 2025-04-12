import uuid
from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel

from app.models.habit import Weekdays


class HabitAdd(BaseModel):
    name: str
    frequency: List[Weekdays]


class HabitCompletion(BaseModel):
    date_completed: date


class HabitResponse(BaseModel):
    habit_id: uuid.UUID
    name: str
    frequency: List[Weekdays]
    dates_completed: List[HabitCompletion]
    created_at: datetime


class HabitResponseFlat(BaseModel):
    habit_id: uuid.UUID
    name: str
    frequency: List[Weekdays]
    dates_completed: List[date]
    created_at: date


class HabitUpdate(BaseModel):
    name: Optional[str] = None
    frequency: Optional[List[Weekdays]] = None
