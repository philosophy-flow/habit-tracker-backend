from typing import Annotated, Optional
from fastapi import Depends

from app.schemas.token import AuthToken, TokenDict
from app.schemas.user import User
from app.services.auth import (
    authenticate_account,
    register_account,
    verify_account,
    refresh_account,
    access_protected_route,
    get_active_user,
)

AuthDep = Annotated[Optional[TokenDict], Depends(authenticate_account)]
RegisterDep = Annotated[bool, Depends(register_account)]
VerifyDep = Annotated[bool, Depends(verify_account)]
AccessDep = Annotated[str, Depends(access_protected_route)]
RefreshDep = Annotated[Optional[AuthToken], Depends(refresh_account)]
UserDep = Annotated[Optional[User], Depends(get_active_user)]
