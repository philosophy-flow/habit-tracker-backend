import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import login, register, user, habit


load_dotenv(override=True)
CLIENT_URL = str(os.getenv("CLIENT_URL"))


app = FastAPI(openapi_url="/openapi.json", docs_url="/docs", redoc_url="/redoc")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[CLIENT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(login.router)
app.include_router(register.router)
app.include_router(user.router)
app.include_router(habit.router)
