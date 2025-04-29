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


@router.patch("/update-password")
async def update_user_password():
    return
    # - payload comes in with existing pw and new pw
    # - 1st check --> verify db user existence w/ access token
    # - 2nd check --> encrypt plaintext pw, check against db user encrypted pw
    # 3. encrypt new pw, update db user with new encrypted pw


@router.patch("/update-email")
async def update_user_email():
    return
    # - payload comes in with existing email, new email and plaintext pw
    # - 1st check --> verify db user existence w/ access token
    # - 2nd check --> encrypt plaintext pw, check against db user encrypted pw
    # - update db user with new email


@router.patch("/update-username")
async def update_user_username():
    return
    # - payload comes in with existing username, new username and plaintext pw
    # - 1st check --> verify db user existence w/ access token
    # - 2nd check --> encrypt plaintext pw, check against db user encrypted pw
    # - update db user with new username
