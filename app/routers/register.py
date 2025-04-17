import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from app.dependencies.register import (
    RegisterDep,
    VerifyDep,
)


load_dotenv(override=True)
CLIENT_URL = str(os.getenv("CLIENT_URL"))

router = APIRouter()


@router.post("/register")
async def register_account(confirmation: RegisterDep):
    if not confirmation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to register account.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"message": "Account created; check email to verify."}


@router.get("/verify")
async def verify_account(confirmation: VerifyDep):
    if not confirmation:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to verify account.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return RedirectResponse(
        url=f"{CLIENT_URL}/login", status_code=status.HTTP_303_SEE_OTHER
    )
