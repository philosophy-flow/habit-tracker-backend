import uuid
from pydantic import BaseModel, EmailStr
from typing import Optional

# from app.schemas.token import AuthToken


class User(BaseModel):
    user_id: uuid.UUID
    email: EmailStr
    username: str
    profile_image_url: Optional[str] = None
    account_verified: bool = False


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str


# class UserAuthenticate(BaseModel):
#     token: AuthToken
#     user: User
