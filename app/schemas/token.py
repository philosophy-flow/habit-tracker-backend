from pydantic import BaseModel
from typing import Optional


class AuthToken(BaseModel):
    access_token: str
    token_type: str


class VerifyToken(BaseModel):
    verify_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: str
    token_type: str


class TokenDict(BaseModel):
    auth: AuthToken
    refresh: RefreshToken


class TokenData(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
