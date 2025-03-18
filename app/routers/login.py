from fastapi import APIRouter, HTTPException, Response, status
from app.dependencies.login import AuthDep, RefreshDep


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


@router.get("/refresh")
async def refresh_account(token: RefreshDep):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired or invalid token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@router.post("/logout")
async def logout_account():
    print("logging out...")
