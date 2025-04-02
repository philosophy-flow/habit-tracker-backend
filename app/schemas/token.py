from pydantic import BaseModel


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
