
from bson import ObjectId
from fastapi import HTTPException, status

from app.models.book_model import BOOK_COLLECTION, book_helper
from app.schemas.book_schema import BookCreate


async def create_book(db, book: BookCreate):
    book_data = book.model_dump()

    result = await db[BOOK_COLLECTION].insert_one(book_data)

    created_book = await db[BOOK_COLLECTION].find_one(
        {"_id": result.inserted_id}
    )

    return book_helper(created_book)


async def get_all_books(db):
    books = []

    async for book in db[BOOK_COLLECTION].find():
        books.append(book_helper(book))

    return books


async def get_book_by_id(db, book_id: str):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid book ID"
        )

    book = await db[BOOK_COLLECTION].find_one(
        {"_id": ObjectId(book_id)}
    )

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    return book_helper(book)


async def update_book(db, book_id: str, book: BookCreate):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid book ID"
        )

    result = await db[BOOK_COLLECTION].update_one(
        {"_id": ObjectId(book_id)},
        {"$set": book.model_dump()}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    updated_book = await db[BOOK_COLLECTION].find_one(
        {"_id": ObjectId(book_id)}
    )

    return book_helper(updated_book)


async def delete_book(db, book_id: str):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid book ID"
        )

    result = await db[BOOK_COLLECTION].delete_one(
        {"_id": ObjectId(book_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
