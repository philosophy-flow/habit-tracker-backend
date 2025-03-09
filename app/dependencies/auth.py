from typing import Annotated, Optional
from fastapi import Depends

from app.schemas.token import AuthToken

from app.services.auth import (
    authenticate_account,
    register_account,
    verify_account,
    access_protected_route,
)

AuthDep = Annotated[Optional[AuthToken], Depends(authenticate_account)]
RegisterDep = Annotated[bool, Depends(register_account)]
VerifyDep = Annotated[bool, Depends(verify_account)]
AccessDep = Annotated[str, Depends(access_protected_route)]
