import uuid
from datetime import date
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, PrimaryKeyConstraint

if TYPE_CHECKING:
    from app.models.habit import HabitDB


class HabitCompletionDB(SQLModel, table=True):
    __tablename__: str = "habit_completions"
    __table_args__ = (PrimaryKeyConstraint("habit_id", "date_completed"),)
    habit_id: uuid.UUID = Field(foreign_key="habits.habit_id", ondelete="CASCADE")
    habit: "HabitDB" = Relationship(back_populates="dates_completed")
    date_completed: date = Field(default_factory=date.today)
