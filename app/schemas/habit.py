import uuid
from pydantic import BaseModel


class HabitAdd(BaseModel):
    name: str
    user_id: uuid.UUID
