import uuid
from typing import List
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
