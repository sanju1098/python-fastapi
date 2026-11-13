
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.connection import (
    connect_to_mongodb,
    close_mongodb_connection
)
from app.routes.book_routes import router as book_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb(app)

    yield

    await close_mongodb_connection(app)


app = FastAPI(
    title="Book Management API",
    description="FastAPI CRUD application with MongoDB",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def home():
    return {
        "message": "FastAPI MongoDB application is running"
    }


app.include_router(book_router)
