from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class AuthToken(BaseModel):
    access_token: str
    token_type: str


class VerifyToken(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
