from fastapi import APIRouter, HTTPException, status
from app.dependencies.auth import AuthDep, RegisterDep, VerifyDep, AccessDep
from app.schemas.token import AuthToken

router = APIRouter()


@router.post("/authenticate", response_model=AuthToken)
async def authenticate_account(token: AuthDep):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@router.post("/register")
async def register_account(confirmation: RegisterDep):
    if not confirmation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to register account",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Account created; check email to verify."}


@router.get("/verify")
async def verify_account(confirmation: VerifyDep):
    if not confirmation:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to verify account",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Account verified successfully."}


@router.get("/protected-route-test")
async def token_test(authenticated: AccessDep):
    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "you're authenticated, yo!"}
