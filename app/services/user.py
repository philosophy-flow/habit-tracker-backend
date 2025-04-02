from typing import Optional
from fastapi import Depends

from app.schemas.user import User
from app.utils.auth import (
    get_user,
)
from app.dependencies.sub import TokenDep, SessionDep


def get_active_user(token: TokenDep, db: SessionDep) -> Optional[User]:
    active_user: Optional[User] = get_user(token, db, "access")
    if not active_user:
        return None
    return active_user
