from typing import Annotated, Optional
from fastapi import Depends, BackgroundTasks, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.models import UserDB
from app.schemas.user import UserRegister
from app.schemas.token import TokenData, AuthToken, VerifyToken
from app.utils.auth import (
    generate_access_token,
    verify_password,
    decode_token,
    generate_password_hash,
    generate_verification_email,
    send_verification_email,
    get_user,
    get_temp_user,
)
from app.db.session import SessionDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authenticate")
TokenDep = Annotated[str, Depends(oauth2_scheme)]
FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


def authenticate_account(
    form_data: FormDep, db: SessionDep, response: Response
) -> Optional[AuthToken]:
    user: Optional[UserDB] = get_user(db, form_data.username)
    if (
        not user
        or not verify_password(form_data.password, user.password_hash)
        or not user.account_verified
    ):
        return None

    auth_jwt = generate_access_token(
        data={"username": user.username, "email": user.email}, token_type="auth"
    )
    auth_token = AuthToken(auth_token=auth_jwt, token_type="bearer")

    refresh_jwt = generate_access_token(
        data={"username": user.username, "email": user.email}, token_type="refresh"
    )

    # response.set_cookie(
    #     key="refresh_token",
    #     value=refresh_jwt,
    #     httponly=True,
    #     secure=True,
    #     samesite="strict",
    #     max_age=7 * 24 * 60 * 60,
    # )

    return auth_token


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
    user: Optional[UserDB] = get_temp_user(token, db)
    if not user:
        return None

    user.account_verified = True
    db.commit()

    return user.account_verified


def access_protected_route(token: TokenDep, db: SessionDep):
    payload = decode_token(token, "auth")
    email = payload.get("email") if payload else None
    username = payload.get("username") if payload else None
    if email is None or username is None:
        return None

    token_data = TokenData(username=username, email=email)
    user: Optional[UserDB] = get_user(
        db, email=token_data.email, username=token_data.username
    )
    if user is None:
        return None
    return user
