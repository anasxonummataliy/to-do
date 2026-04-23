from contextlib import asynccontextmanager

from fastapi.security import HTTPBearer
from app.database.init_db import create_tables
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router

auth_scheme = HTTPBearer(auto_error=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title="Auth API",
    description="Auth API",
    version="1.0.0",
    lifespan=lifespan,
    dependencies=[Depends(auth_scheme)],
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def start():
    return {"message": "Server is working!"}


app.include_router(api_router)
