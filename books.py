# FastAPI - Books API

from fastapi import Body, FastAPI

app = FastAPI()


# -------------------- Basic API --------------------
@app.get("/")
async def first_api():
    # async is optional; use it when working with asynchronous operations
    return {"message": "Hello FastAPI"}


# Start server: uvicorn books:app --reload
# Development server: fastapi dev books.py
# Production server: fastapi run books.py


# -------------------- Books Data --------------------
BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


# -------------------- GET APIs --------------------
# Get all books
@app.get("/books")
async def read_all_books():
    return BOOKS


# Swagger UI: http://127.0.0.1:8000/docs


# -------------------- Path Parameters --------------------
# Path parameters are dynamic values passed directly through the URL.
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        # casefold() performs case-insensitive comparison
        if book.get('title').casefold() == book_title.casefold():
            return book


# -------------------- Query Parameters --------------------
# Query parameters are passed after '?' in key=value format.
@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []

    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


# Get books by author using a query parameter
@app.get("/books/byauthor/")
async def read_books_by_author_path(author: str):
    books_to_return = []

    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)

    return books_to_return


# Get books by author and category using path + query parameters
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []

    for book in BOOKS:
        if (
            book.get('author').casefold() == book_author.casefold()
            and book.get('category').casefold() == category.casefold()
        ):
            books_to_return.append(book)

    return books_to_return


# -------------------- POST API --------------------
# Create a new book using the request body.
# Example: {"title": "New Book", "author": "Sanjay", "category": "software"}
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


# -------------------- PUT API --------------------
# Update an existing book based on its title.
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            break


# -------------------- DELETE API --------------------
# Delete a book based on its title.
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break


# ====================================================
# ASSIGNMENT
# ====================================================

# Create a new API endpoint to fetch all books
# written by a specific author.
#
# Implement using either:
# 1. Path Parameters
# 2. Query Parameters
#
# Expected result: Return all matching books.


# Solution: Using Query Parameters
@app.get("/books/byauthor/")
async def read_books_by_author_query(author: str):
    books_to_return = []

    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)

    return books_to_return
