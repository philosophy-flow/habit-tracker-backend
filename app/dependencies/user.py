from typing import Annotated, Optional
from fastapi import Depends

from app.schemas.user import User
from app.services.user import (
    get_active_user,
)

UserDep = Annotated[Optional[User], Depends(get_active_user)]
