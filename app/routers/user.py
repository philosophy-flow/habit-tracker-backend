from fastapi import APIRouter, HTTPException, status
from app.dependencies.user import (
    UserDep,
)


router = APIRouter()


@router.get("/user")
async def get_active_user(user: UserDep):
    return user


@router.get("/reset-password")
async def reset_user_password():
    print("resetting password...")
