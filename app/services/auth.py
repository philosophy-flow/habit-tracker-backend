from typing import Annotated, Optional
from fastapi import Depends, BackgroundTasks, Cookie
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.models import UserDB
from app.schemas.user import UserRegister
from app.schemas.token import TokenData, AuthToken, VerifyToken, RefreshToken, TokenDict
from app.utils.auth import (
    generate_access_token,
    verify_password,
    decode_token,
    generate_password_hash,
    generate_verification_email,
    send_verification_email,
    get_db_user,
    get_user,
)
from app.db.session import SessionDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authenticate")
TokenDep = Annotated[str, Depends(oauth2_scheme)]
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


def register_account(
    user: UserRegister, db: SessionDep, background_tasks: BackgroundTasks
):
    if not user:
        return None

    temp_user = UserDB(
        email=user.email,
        username=user.username,
        password_hash=generate_password_hash(user.password),
        account_verified=False,
    )

    db.add(temp_user)
    db.commit()
    db.refresh(temp_user)

    verify_jwt = generate_access_token(
        data={"username": user.username, "email": user.email}, token_type="verify"
    )
    verify_token = VerifyToken(verify_token=verify_jwt, token_type="bearer")

    verification_email = generate_verification_email(user, verify_token)
    send_verification_email(verification_email, background_tasks)

    return True


def verify_account(token: str, db: SessionDep):
    user = get_user(token, db, "verify")
    if not user:
        return None

    user.account_verified = True
    db.commit()

    return user.account_verified


def refresh_account(refresh_token: Annotated[str, Cookie()], db: SessionDep):
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
