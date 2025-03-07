from typing import Annotated, Optional
from fastapi import Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.models import UserDB
from app.schemas.user import User, UserRegister, UserAuthenticate
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
    form_data: FormDep, db: SessionDep
) -> Optional[UserAuthenticate]:
    user: Optional[UserDB] = get_user(db, form_data.username)
    if (
        not user
        or not verify_password(form_data.password, user.password_hash)
        or not user.account_verified
    ):
        return None

    access_jwt = generate_access_token(
        data={"username": user.username, "email": user.email}, token_type="auth"
    )
    auth_access_token = AuthToken(access_token=access_jwt, token_type="bearer")

    authenticated_user = User(
        user_id=user.user_id,
        email=user.email,
        username=user.username,
        profile_image_url=user.profile_image_url,
        account_verified=user.account_verified,
    )

    return UserAuthenticate(token=auth_access_token, user=authenticated_user)


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
    verify_access_token = VerifyToken(access_token=verify_jwt, token_type="bearer")

    verification_email = generate_verification_email(user, verify_access_token)
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
