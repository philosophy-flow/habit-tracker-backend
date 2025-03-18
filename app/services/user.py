from typing import Annotated, Optional
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.models import UserDB
from app.schemas.token import TokenData
from app.utils.auth import (
    decode_token,
    get_db_user,
    get_user,
)
from app.db.session import SessionDep


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authenticate")
TokenDep = Annotated[str, Depends(oauth2_scheme)]
FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


def get_active_user(token: TokenDep, db: SessionDep):
    active_user = get_user(token, db, "access")
    if not active_user:
        return None
    return active_user


def access_protected_route(token: TokenDep, db: SessionDep):
    payload = decode_token(token, "access")
    email = payload.get("email") if payload else None
    username = payload.get("username") if payload else None
    if email is None or username is None:
        return None

    token_data = TokenData(username=username, email=email)
    user: Optional[UserDB] = get_db_user(
        db, email=token_data.email, username=token_data.username
    )
    if user is None:
        return None
    return user
