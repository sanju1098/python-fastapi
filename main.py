import os
from contextlib import asynccontextmanager

from bson import ObjectId
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field
from pymongo import AsyncMongoClient
from typing import Optional

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")


# ---------------- DATABASE CONNECTION ----------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = AsyncMongoClient(MONGODB_URL)
    app.database = app.mongodb_client[DATABASE_NAME]

    await app.database.command("ping")
    print("Connected to MongoDB successfully!")

    yield

    await app.mongodb_client.close()
    print("MongoDB connection closed!")


app = FastAPI(lifespan=lifespan)


# ---------------- PYDANTIC MODELS ----------------

class BookCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    author: str = Field(min_length=2, max_length=50)
    description: str = Field(min_length=5, max_length=200)
    rating: int = Field(ge=0, le=5)
    published_year: int = Field(ge=2000, le=2030)

class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None,min_length=3,max_length=100)
    author: Optional[str] = Field(default=None,min_length=2,max_length=50)
    description: Optional[str] = Field(default=None,min_length=5,max_length=200)
    rating: Optional[int] = Field(default=None,ge=0,le=5)
    published_year: Optional[int] = Field(default=None,ge=2000,le=2030)

class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    description: str
    rating: int
    published_year: int


# ---------------- HELPER FUNCTION ----------------

def book_helper(book) -> dict:
    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "author": book["author"],
        "description": book["description"],
        "rating": book["rating"],
        "published_year": book["published_year"]
    }


# ---------------- HOME API ----------------

@app.get("/")
async def home():
    return {"message": "FastAPI MongoDB application is running"}


# ---------------- CREATE BOOK ----------------

@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    book_data = book.model_dump()
    result = await app.database["books"].insert_one(book_data)
    created_book = await app.database["books"].find_one(
        {"_id": result.inserted_id}
    )

    return book_helper(created_book)


# ---------------- GET ALL BOOKS ----------------

@app.get("/books", response_model=list[BookResponse])
async def get_all_books():
    books = []
    async for book in app.database["books"].find():
        books.append(book_helper(book))
    return books


# ---------------- GET BOOK BY ID ----------------

@app.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_id: str):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid book ID"
        )

    book = await app.database["books"].find_one(
        {"_id": ObjectId(book_id)}
    )

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book_helper(book)


# ---------------- UPDATE BOOK ----------------

@app.put("/books/{book_id}", response_model=BookResponse)
async def update_book(book_id: str, book: BookCreate):

    if not ObjectId.is_valid(book_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid book ID"
        )

    result = await app.database["books"].update_one(
        {"_id": ObjectId(book_id)},
        {"$set": book.model_dump()}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    updated_book = await app.database["books"].find_one(
        {"_id": ObjectId(book_id)}
    )

    return book_helper(updated_book)



# ---------------- UPDATE BOOK (PATCH)----------------

@app.patch("/books/{book_id}", response_model=BookResponse)
async def patch_book(book_id: str, book: BookUpdate):

    # Validate MongoDB ObjectId
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400,detail="Invalid book ID")

    # Get only the fields provided by the client
    update_data = book.model_dump(exclude_unset=True)

    # Check whether the request contains any fields
    if not update_data:
        raise HTTPException(status_code=400,detail="No fields provided for update"
        )

    # Update only the provided fields
    result = await app.database["books"].update_one(
        {"_id": ObjectId(book_id)},
        {"$set": update_data}
    )

    # Check whether book exists
    if result.matched_count == 0:
        raise HTTPException(status_code=404,detail="Book not found")

    # Fetch updated document
    updated_book = await app.database["books"].find_one(
        {"_id": ObjectId(book_id)}
    )

    return book_helper(updated_book)


# ---------------- DELETE BOOK ----------------

@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book(book_id: str):

    if not ObjectId.is_valid(book_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid book ID"
        )

    result = await app.database["books"].delete_one(
        {"_id": ObjectId(book_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

