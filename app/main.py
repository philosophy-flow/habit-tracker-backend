from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth

origins = ["http://localhost:5173"]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
