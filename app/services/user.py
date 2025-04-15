from typing import Optional
from fastapi import Depends

from app.schemas.user import User, UserResponse
from app.utils.auth import (
    get_user,
)
from app.dependencies.shared import TokenDep, SessionDep


def get_active_user(token: TokenDep, db: SessionDep) -> Optional[UserResponse]:
    active_user: Optional[User] = get_user(token, db, "access")
    if not active_user:
        return None

    user_response = UserResponse(**active_user.model_dump(exclude={"habits"}))

    return user_response
