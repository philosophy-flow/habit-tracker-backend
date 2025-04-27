import uuid
from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel, Field

from app.models.habit import Weekdays


class HabitAdd(BaseModel):
    name: str = Field(min_length=1, description="must be non-empty")
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
    name: Optional[str] = Field(
        None, min_length=1, description="if provided, must be at least 1 char"
    )
    frequency: Optional[List[Weekdays]] = None
