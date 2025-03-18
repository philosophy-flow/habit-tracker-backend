from typing import Annotated
from fastapi import Depends

from app.services.register import (
    register_account,
    verify_account,
)


RegisterDep = Annotated[bool, Depends(register_account)]
VerifyDep = Annotated[bool, Depends(verify_account)]
