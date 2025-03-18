from typing import Annotated, Optional
from fastapi import Depends

from app.schemas.user import User
from app.services.user import (
    access_protected_route,
    get_active_user,
)

AccessDep = Annotated[str, Depends(access_protected_route)]
UserDep = Annotated[Optional[User], Depends(get_active_user)]
