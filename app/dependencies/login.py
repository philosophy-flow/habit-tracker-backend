from typing import Annotated, Optional
from fastapi import Depends

from app.schemas.token import TokenDict, AuthToken
from app.services.login import authenticate_account, refresh_account

AuthDep = Annotated[Optional[TokenDict], Depends(authenticate_account)]
RefreshDep = Annotated[Optional[AuthToken], Depends(refresh_account)]
