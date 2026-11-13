
from fastapi import APIRouter, Depends, Response, status

from app.database.connection import get_database
from app.schemas.book_schema import BookCreate, BookResponse
from app.services import book_service

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


@router.post(
    "",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_book(
    book: BookCreate,
    db=Depends(get_database)
):
    return await book_service.create_book(db, book)


@router.get(
    "",
    response_model=list[BookResponse]
)
async def get_all_books(
    db=Depends(get_database)
):
    return await book_service.get_all_books(db)


@router.get(
    "/{book_id}",
    response_model=BookResponse
)
async def get_book(
    book_id: str,
    db=Depends(get_database)
):
    return await book_service.get_book_by_id(db, book_id)


@router.put(
    "/{book_id}",
    response_model=BookResponse
)
async def update_book(
    book_id: str,
    book: BookCreate,
    db=Depends(get_database)
):
    return await book_service.update_book(db, book_id, book)


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book(
    book_id: str,
    db=Depends(get_database)
):
    await book_service.delete_book(db, book_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
