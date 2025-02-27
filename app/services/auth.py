from typing import Annotated, Optional
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import select, or_

from app.models import UserDB
from app.schemas.user import UserRegister
from app.schemas.token import TokenData, AuthToken, VerifyToken
from app.utils.auth import (
    generate_access_token,
    verify_password,
    decode_token,
    generate_password_hash,
)
from app.db.session import SessionDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authenticate")
TokenDep = Annotated[str, Depends(oauth2_scheme)]
FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


def get_user(
    db: SessionDep, username: Optional[str] = None, email: Optional[str] = None
):
    select_user = select(UserDB).where(
        or_(UserDB.username == username, UserDB.email == email)
    )
    return db.exec(select_user).first()


def get_temp_user(token: str, db: SessionDep):
    payload = decode_token(token, "verify")
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


def authenticate_account(form_data: FormDep, db: SessionDep):
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

    return auth_access_token


def register_account(user: UserRegister, db: SessionDep):
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
    print(verify_access_token)

    # send email with embedded jwt; will make GET request to /verify
    return True


def verify_account(token: str, db: SessionDep):
    user: Optional[UserDB] = get_temp_user(token, db)
    if not user:
        return None

    user.account_verified = True
    db.commit()

    return user.account_verified
