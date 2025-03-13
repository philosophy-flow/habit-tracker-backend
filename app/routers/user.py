from fastapi import APIRouter
from app.dependencies.user import UserDep

router = APIRouter()


@router.post("/user")
async def get_user(user: UserDep):
    return user
