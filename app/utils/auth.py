import jwt
from jwt.exceptions import InvalidTokenError, InvalidSignatureError
from datetime import datetime, timedelta, timezone
from sqlmodel import select, or_
from typing import Literal, Optional, Union, overload

from app.config.auth import (
    jwt_auth_config,
    jwt_verify_config,
    jwt_refresh_config,
)
from app.models import UserDB
from app.schemas.user import User


def get_db_user(
    db,
    username=None,
    email=None,
) -> Optional[UserDB]:
    select_user = select(UserDB).where(
        or_(UserDB.username == username, UserDB.email == email)
    )
    return db.exec(select_user).first()


@overload
def get_user(token, db, type: Literal["verify"]) -> Optional[UserDB]: ...
@overload
def get_user(token, db, type: Literal["access"]) -> Optional[User]: ...
@overload
def get_user(token, db, type: Literal["refresh"]) -> Optional[User]: ...
def get_user(token, db, type) -> Union[UserDB, User, None]:
    payload = decode_token(token, type)
    email = payload.get("email") if payload else None
    username = payload.get("username") if payload else None

    if email is None or username is None:
        return None

    user: Optional[UserDB] = get_db_user(
        db,
        email=email,
        username=username,
    )

    if user is None:
        return None
    elif type == "verify":
        return user
    elif type == "access" or type == "refresh":
        return User(
            user_id=user.user_id,
            email=user.email,
            username=user.username,
            profile_image_url=user.profile_image_url,
            account_verified=user.account_verified,
        )


def generate_access_token(data, token_type):
    if token_type == "access":
        token_config = jwt_auth_config
    elif token_type == "verify":
        token_config = jwt_verify_config
    elif token_type == "refresh":
        token_config = jwt_refresh_config

    to_encode = data.copy()

    if token_config["time_diff"]:
        expire = datetime.now(timezone.utc) + token_config["time_diff"]
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=5)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, token_config["key"], algorithm=token_config["algorithm"]
    )

    return encoded_jwt


def decode_token(token, token_type):
    if token_type == "access":
        key = jwt_auth_config["key"]
        algorithm = jwt_auth_config["algorithm"]
    elif token_type == "verify":
        key = jwt_verify_config["key"]
        algorithm = jwt_verify_config["algorithm"]
    elif token_type == "refresh":
        key = jwt_refresh_config["key"]
        algorithm = jwt_refresh_config["algorithm"]

    try:
        return jwt.decode(token, key, algorithms=algorithm)
    except InvalidSignatureError:
        return None
    except InvalidTokenError:
        return None
