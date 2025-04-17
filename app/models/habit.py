import uuid
from enum import Enum
from datetime import datetime, timezone
from typing import List, Union, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column
from sqlalchemy.types import JSON

if TYPE_CHECKING:
    from app.models.user import UserDB
    from app.models.habit_completion import HabitCompletionDB


class Weekdays(str, Enum):
    Sun = "Sun"
    Mon = "Mon"
    Tue = "Tue"
    Wed = "Wed"
    Thu = "Thu"
    Fri = "Fri"
    Sat = "Sat"


class HabitDB(SQLModel, table=True):
    __table_args__ = {"schema": "habitsior"}
    __tablename__: str = "habits"
    habit_id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str = Field(max_length=50, nullable=False)
    user_id: uuid.UUID = Field(
        foreign_key="habitsior.users.user_id", ondelete="CASCADE", nullable=False
    )
    user: "UserDB" = Relationship(back_populates="habits")
    frequency: List[Weekdays] = Field(sa_column=Column(JSON))
    dates_completed: List["HabitCompletionDB"] = Relationship(
        back_populates="habit", cascade_delete=True
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
