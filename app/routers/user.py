from fastapi import APIRouter, HTTPException, status
from app.dependencies.user import (
    UserDep,
)


router = APIRouter()


@router.get("/user")
async def get_active_user(user: UserDep):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired or invalid token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@router.get("/reset-password")
async def reset_user_password():
    print("resetting password...")
