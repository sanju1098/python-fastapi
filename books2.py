from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status


app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int


    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


# Pydantics => Python library that is used for data modeling, data parsing and has efficient error handling
# Pydantics is commonly used as a resource for data validation and how to handle data coming to our FastAPI application

# Create a different request model for data validation
# Field data validation on each variable/element

# from pydantic import BaseModel => Import statement

# class BookRequest(BaseModel):
#     id: int
#     title: str
#     author: str
#     description: str
#     rating: int

# Adding Validation - Filed from pydantic
class BookRequest(BaseModel):
    # id: int
    # id: Optional[int] = None
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6) #(0 to 6); if went from 1 then gt=0
    published_date: int = Field(gt=1999, lt=2031)
    
    # To pre-populate some JSON in the swagger (like example with proper data) instead of string
    model_config = {
        "json_schema_extra": {
            "example" : {
                "title": "Book title",
                "author": "Name of the Author",
                "description": "Description of the book",
                "rating": "Book rating",
                "published_date": "Date of book published",
            }
        }
    }

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]


@app.get("/books/", status_code = status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/book/{book_id}", status_code = status.HTTP_200_OK)
# async def read_all_books(book_id: int):
async def read_book(book_id: int = Path(gt=0)): # validations
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Not Found") # HTTP Exceptions


@app.get("/books", status_code = status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=-1, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/publish", status_code = status.HTTP_200_OK)
async def read_book_by_publish_date(published_date: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.get("/books", status_code = status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

def find_book_id(book: Book):
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id+1
    # else:
    #     book.id = 1
    # return book
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1 # short way 

    
@app.post("/create-book", status_code = status.HTTP_201_CREATED)
# async def create_book(book_request=Body()):
    # BOOKS.append(book_request)

async def create_book(book_request: BookRequest): # after creating BookRequest
    new_book = Book(**book_request.dict()) # this turn into dictionary
    # BOOKS.append(new_book)
    BOOKS.append(find_book_id(new_book)) # over ride book id - even if we pass 0 


@app.put("/books/update_book", status_code = status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed: # HTTP Exceptions
        HTTPException(status_code=404, detail="Book Not Found") 
    

@app.delete("/books/{book_id}", status_code = status.HTTP_204_NO_CONTENT)
# async def delete_book(book_id: int):
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break;
    if not book_changed: # HTTP Exceptions
        HTTPException(status_code=404, detail="Book Not Found") 


"""
STATUS CODE
An HTTP Status Code is used to help the client (the user or system submitting data to server) to understand what happened on the server side application
"""