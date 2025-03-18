from fastapi import APIRouter, HTTPException, Response, status
from app.dependencies.auth import (
    AuthDep,
    RegisterDep,
    VerifyDep,
    AccessDep,
    RefreshDep,
    UserDep,
)

router = APIRouter()


@router.post("/authenticate")
async def authenticate_account(tokens: AuthDep, response: Response):
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh.refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=int(3.5 * 24 * 60 * 60),
    )

    return tokens.auth


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


@router.get("/refresh")
async def refresh_account(token: RefreshDep):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired or invalid token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@router.get("/user")
async def get_active_user(user: UserDep):
    return user


@router.get("/protected-route-test")
async def token_test(authenticated: AccessDep):
    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "you're authenticated, yo!"}
