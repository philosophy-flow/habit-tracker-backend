from fastapi import FastAPI
from app.db.session import SessionDep
from app.models.user import UserDB
from app.routers import auth

from app.utils.auth import generate_password_hash


app = FastAPI()
app.include_router(auth.router)
