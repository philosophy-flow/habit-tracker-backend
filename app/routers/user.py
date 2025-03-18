from fastapi import APIRouter, HTTPException, status
from app.dependencies.user import (
    AccessDep,
    UserDep,
)


router = APIRouter()


@router.get("/user")
async def get_active_user(user: UserDep):
    return user


@router.get("/reset-password")
async def reset_user_password():
    print("resetting password...")


@router.get("/protected-route-test")
async def token_test(authenticated: AccessDep):
    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "you're authenticated, yo!"}
