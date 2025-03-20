from typing import Annotated, Optional
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.schemas.user import User
from app.utils.auth import (
    get_user,
)
from app.db.session import SessionDep


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authenticate")
TokenDep = Annotated[str, Depends(oauth2_scheme)]
FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


def get_active_user(token: TokenDep, db: SessionDep) -> Optional[User]:
    active_user: Optional[User] = get_user(token, db, "access")
    if not active_user:
        return None
    return active_user
