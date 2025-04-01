import uuid
from datetime import datetime, timezone
from typing import List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import UserDB
    from app.models.habit_completion import HabitCompletionDB


class HabitDB(SQLModel, table=True):
    __tablename__: str = "habits"
    habit_id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str = Field(max_length=50, nullable=False)
    user_id: uuid.UUID = Field(
        foreign_key="users.user_id", ondelete="CASCADE", nullable=False
    )
    user: "UserDB" = Relationship(back_populates="habits")
    dates_completed: List["HabitCompletionDB"] = Relationship(back_populates="habit")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
