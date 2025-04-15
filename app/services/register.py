from fastapi import BackgroundTasks
from typing import Optional

from app.models import UserDB
from app.schemas.user import UserRegister
from app.schemas.token import VerifyToken
from app.utils.auth import (
    generate_access_token,
    get_user,
)
from app.utils.verify import (
    generate_password_hash,
    generate_verification_email,
    send_verification_email,
)
from app.dependencies.shared import SessionDep


def register_account(
    user: Optional[UserRegister], db: SessionDep, background_tasks: BackgroundTasks
) -> bool:
    if not user:
        return False

    try:
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
        verify_token = VerifyToken(verify_token=verify_jwt, token_type="verify")

        verification_email = generate_verification_email(user, verify_token)
        send_verification_email(verification_email, background_tasks)
    except:
        return False

    return True


def verify_account(token: str, db: SessionDep) -> bool:
    user = get_user(token, db, "verify")
    if not user:
        return False

    user.account_verified = True
    db.commit()

    return user.account_verified
