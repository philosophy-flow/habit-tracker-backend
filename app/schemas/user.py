import uuid
from pydantic import BaseModel, EmailStr
from typing import Optional, List

from app.schemas.habit import HabitResponseFlat


class User(BaseModel):
    user_id: uuid.UUID
    email: EmailStr
    username: str
    profile_image_url: Optional[str] = None
    account_verified: bool = False
    habits: List[HabitResponseFlat] = []


class UserResponse(BaseModel):
    user_id: uuid.UUID
    email: EmailStr
    username: str
    profile_image_url: Optional[str] = None
    account_verified: bool = False


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
