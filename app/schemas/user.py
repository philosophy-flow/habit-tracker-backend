import uuid
from pydantic import BaseModel, EmailStr, Field, field_validator
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
    username: str = Field(
        min_length=3,
        max_length=20,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9_]*[A-Za-z0-9]$",
        description="3-20 chars; letters, numbers, underscores; no leading or trailing underscore",
    )
    password: str = Field(
        min_length=8,
        description="min 8 chars; must contain at least 1 uppercase letter, number, and symbol",
    )

    @field_validator("password")
    @classmethod
    def check_password(cls, pwd: str) -> str:
        if not any(ch.isupper() for ch in pwd):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(ch.isdigit() for ch in pwd):
            raise ValueError("Password must contain at least one digit")
        if not any(not ch.isalnum() for ch in pwd):
            raise ValueError("Password must contain at least one symbol")
        return pwd
