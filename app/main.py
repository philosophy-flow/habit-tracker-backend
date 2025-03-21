from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import login, register, user


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(login.router)
app.include_router(register.router)
app.include_router(user.router)
