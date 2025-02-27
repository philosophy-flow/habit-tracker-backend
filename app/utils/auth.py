import os
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv(override=True)
JWT_VERIFY_KEY = os.getenv("JWT_VERIFY_KEY")
JWT_VERIFY_MINUTES = float(os.getenv("JWT_VERIFY_EXPIRE_MINUTES", "5"))
JWT_AUTH_KEY = os.getenv("JWT_AUTH_KEY")
JWT_AUTH_MINUTES = float(os.getenv("JWT_AUTH_EXPIRE_MINUTES", "20"))
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

jwt_verify_config = {
    "key": JWT_VERIFY_KEY,
    "time_diff": timedelta(minutes=JWT_VERIFY_MINUTES),
}

jwt_auth_config = {
    "key": JWT_AUTH_KEY,
    "time_diff": timedelta(minutes=JWT_AUTH_MINUTES),
}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def generate_password_hash(password):
    return pwd_context.hash(password)


def generate_access_token(data: dict, token_type: str):
    if token_type == "auth":
        token_config = jwt_auth_config
    elif token_type == "verify":
        token_config = jwt_verify_config

    to_encode = data.copy()
    if token_config["time_diff"]:
        expire = datetime.now(timezone.utc) + token_config["time_diff"]
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=5)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, token_config["key"], algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_token(token, token_type: str):
    if token_type == "auth":
        key = jwt_auth_config["key"]
    elif token_type == "verify":
        key = jwt_verify_config["key"]

    try:
        return jwt.decode(token, key, algorithms=[JWT_ALGORITHM])
    except InvalidTokenError:
        return None
