import uuid
from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.habit import HabitDB


class UserDB(SQLModel, table=True):
    __tablename__: str = "users"
    user_id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    email: str = Field(unique=True, max_length=255, nullable=False)
    username: str = Field(unique=True, max_length=50, nullable=False)
    password_hash: str = Field(max_length=255, nullable=False)
    profile_image_url: Optional[str] = Field(default=None, max_length=512)
    habits: List["HabitDB"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"order_by": "HabitDB.name"}
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    account_verified: bool = Field(default=False, nullable=False)
