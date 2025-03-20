from typing import Annotated, Optional
from fastapi import Depends, Cookie
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.token import AuthToken, RefreshToken, TokenDict
from app.utils.auth import (
    generate_access_token,
    get_db_user,
    get_user,
)
from app.utils.verify import verify_password
from app.db.session import SessionDep


FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


def authenticate_account(form_data: FormDep, db: SessionDep) -> Optional[TokenDict]:
    user = get_db_user(db, form_data.username)
    if (
        not user
        or not verify_password(form_data.password, user.password_hash)
        or not user.account_verified
    ):
        return None

    auth_jwt = generate_access_token(
        data={"username": user.username, "email": user.email}, token_type="access"
    )
    auth_token = AuthToken(access_token=auth_jwt, token_type="bearer")

    refresh_jwt = generate_access_token(
        data={"username": user.username, "email": user.email}, token_type="refresh"
    )
    refresh_token = RefreshToken(refresh_token=refresh_jwt, token_type="refresh")

    tokens = TokenDict(auth=auth_token, refresh=refresh_token)
    return tokens


def refresh_account(
    db: SessionDep,
    refresh_token: Annotated[Optional[str], Cookie()] = None,
) -> Optional[AuthToken]:
    refresh_user = get_user(refresh_token, db, "refresh")

    if refresh_user:
        access_jwt = generate_access_token(
            data={"username": refresh_user.username, "email": refresh_user.email},
            token_type="access",
        )
        auth_token = AuthToken(access_token=access_jwt, token_type="bearer")
        return auth_token
    else:
        return None
