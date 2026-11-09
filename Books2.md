# FastAPI – Pydantic, Data Validation & HTTP Status Codes

This section covers the next level of FastAPI development by introducing data validation, request models, parameter validation, exception handling, and HTTP status codes.

We will continue using the Books API to understand these concepts practically.

# 1. Introduction to Pydantic

Pydantic is a Python library used for data validation, parsing, and serialization.

It is commonly used with FastAPI to validate data coming into the application.

### Why do we need Pydantic?

Consider a scenario where a frontend application sends book information to our FastAPI backend.

The expected request body is:

```json
{
    "title": "FastAPI Book",
    "author": "Sanjay",
    "description": "Learning FastAPI",
    "rating": 5,
    "published_date": 2025
}
```

But what if the frontend sends:

```json
{
    "title": "AB",
    "author": "",
    "description": "Learning FastAPI",
    "rating": 10,
    "published_date": 1990
}
```

This request contains invalid data according to our requirements.

Without proper validation, we would need to write manual validation logic for every field.

Pydantic solves this problem by validating incoming data based on the rules we define.

### Key Responsibilities of Pydantic

- Validates incoming request data.
- Checks data types.
- Applies field-level validation rules.
- Generates meaningful validation errors.
- Helps define the expected structure of request data.

**Important:** FastAPI integrates with Pydantic to automatically validate request bodies and generate API documentation.

---

# 2. Python Class vs Pydantic Model

In this project, we use two different types of classes:

1. Normal Python class – `Book`
2. Pydantic model – `BookRequest`

Understanding the difference is important.

### A. Normal Python Class

```python
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
```

**Explanation:**

- `class Book`: Creates a normal Python class.
- Variables represent the properties of a book.
- `__init__()` is the constructor.
- The constructor initializes the object when a new Book instance is created.
- `self` refers to the current object.

Example:

```python
book = Book(
    1,
    "FastAPI Book",
    "Sanjay",
    "Learning FastAPI",
    5,
    2025
)
```

Here, we create an object of the Book class.

**Important:** A normal Python class does not automatically perform Pydantic validation. The type annotations alone do not enforce the field types.

### B. Pydantic Model

```python
from pydantic import BaseModel

class BookRequest(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int
```

**Explanation:**

- `BaseModel` is imported from Pydantic.
- `BookRequest` inherits from `BaseModel`.
- Each variable represents a field in the request model.
- Pydantic automatically validates incoming data based on the defined types.

For example, if the API expects `rating` to be an integer but receives an incompatible value, Pydantic generates a validation error.

### Difference Between Book and BookRequest

| Book | BookRequest |
|---|---|
| Normal Python class | Pydantic model |
| Used to represent book objects in our example | Used to validate incoming request data |
| Does not automatically validate types | Automatically validates data |
| Uses `__init__()` constructor | Uses Pydantic's model initialization |
| Does not inherit from BaseModel | Inherits from BaseModel |

**Simple understanding:**

- `Book` → Represents the book object stored in our application.
- `BookRequest` → Defines and validates the structure of data coming from the client.

---

# 3. BaseModel

`BaseModel` is the foundation of Pydantic models.

Whenever we want to create a Pydantic model, we inherit from `BaseModel`.

### Syntax

```python
from pydantic import BaseModel

class BookRequest(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int
```

### Example Request Body

```json
{
    "id": 1,
    "title": "FastAPI Book",
    "author": "Sanjay",
    "description": "Learning FastAPI",
    "rating": 5,
    "published_date": 2025
}
```

FastAPI uses the BookRequest model to validate the incoming JSON.

If the request satisfies the model's validation rules, the endpoint receives the validated data.

Otherwise, FastAPI automatically returns a validation error, generally with HTTP status code `422 Unprocessable Entity`.

### Why is BaseModel important?

Without Pydantic models, we would need to manually extract and validate each field from the request body.

Using BaseModel makes the code cleaner and validation easier to maintain.

---

# 4. Field() – Field-Level Data Validation

Pydantic provides `Field()` to define additional validation rules and metadata for individual fields.

Import:

```python
from pydantic import BaseModel, Field
```

### BookRequest Model with Validation

```python
from typing import Optional
from pydantic import BaseModel, Field

class BookRequest(BaseModel):

    id: Optional[int] = Field(
        description="ID is not needed on create",
        default=None
    )

    title: str = Field(min_length=3)

    author: str = Field(min_length=1)

    description: str = Field(
        min_length=1,
        max_length=100
    )

    rating: int = Field(gt=-1, lt=6)

    published_date: int = Field(gt=1999, lt=2031)
```

Let's understand each validation.

### A. title

```python
title: str = Field(min_length=3)
```

- Data type must be a string.
- Minimum length should be 3 characters.

Valid:

```json
{
    "title": "Python"
}
```

Invalid:

```json
{
    "title": "AB"
}
```

### B. author

```python
author: str = Field(min_length=1)
```

- Data type must be a string.
- Minimum length should be 1 character.

An empty string is not accepted.

### C. description

```python
description: str = Field(min_length=1, max_length=100)
```

- Minimum length: 1 character.
- Maximum length: 100 characters.

This ensures that the description stays within the specified length.

### D. rating

```python
rating: int = Field(gt=-1, lt=6)
```

Here, we are using comparison constraints.

| Validation | Meaning |
|---|---|
| `gt` | Greater than |
| `lt` | Less than |
| `ge` | Greater than or equal to |
| `le` | Less than or equal to |

Our validation:

```python
Field(gt=-1, lt=6)
```

Means:

- Rating must be greater than -1.
- Rating must be less than 6.

Therefore, valid integer ratings are:

```text
0, 1, 2, 3, 4, 5
```

If you want ratings from 1 to 5:

```python
rating: int = Field(gt=0, le=5)
```

### E. published_date

```python
published_date: int = Field(gt=1999, lt=2031)
```

This means:

- Published year must be greater than 1999.
- Published year must be less than 2031.

Valid values:

```text
2000 to 2030
```

### Field Validation Summary

| Field | Validation | Accepted Values |
|---|---|---|
| title | `min_length=3` | At least 3 characters |
| author | `min_length=1` | At least 1 character |
| description | `min_length=1, max_length=100` | 1–100 characters |
| rating | `gt=-1, lt=6` | Integers 0–5 |
| published_date | `gt=1999, lt=2031` | Integers 2000–2030 |

**Important:** Pydantic validates incoming data according to the defined rules. If validation fails, FastAPI rejects the request before executing the endpoint function.

---

# 5. Optional Fields

Sometimes a field is not mandatory.

For example, when creating a book, we might not want the frontend to provide the book ID because the backend can generate it automatically.

For this purpose, we use Optional.

### Import

```python
from typing import Optional
```

### Example

```python
id: Optional[int] = None
```

This means:

- ID can contain an integer.
- ID can also be `None`.
- If the client does not provide an ID, its default value will be `None`.

### Using Field() with Optional

```python
id: Optional[int] = Field(
    description="ID is not needed on create",
    default=None
)
```

Here:

- `Optional[int]` means the value can be an integer or None.
- `description` provides information about the field.
- `default=None` makes the field optional when submitting a request.

### Example Request Without ID

```json
{
    "title": "FastAPI Book",
    "author": "Sanjay",
    "description": "Learning FastAPI",
    "rating": 5,
    "published_date": 2025
}
```

This request is valid because ID is optional.

**Important distinction:**

`Optional[int]` alone means a field accepts an integer or None. To make it optional to omit from the request, give it a default value such as `None`.

---

# 6. model_config – Pre-populating Swagger Examples

FastAPI automatically generates Swagger documentation.

We can also provide example request data so developers can understand the expected request structure.

Pydantic provides `model_config` for this.

### Example

```python
class BookRequest(BaseModel):

    id: Optional[int] = Field(default=None)

    title: str = Field(min_length=3)

    author: str = Field(min_length=1)

    description: str = Field(min_length=1, max_length=100)

    rating: int = Field(gt=-1, lt=6)

    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Book title",
                "author": "Name of the Author",
                "description": "Description of the book",
                "rating": 5,
                "published_date": 2025
            }
        }
    }
```

### What does this do?

- `model_config` defines Pydantic model configuration.
- `json_schema_extra` provides additional JSON Schema information.
- `example` provides sample request data.

When you open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

You can see the example request body for the API.

**Why is this useful?**

Instead of showing an empty or confusing request body, Swagger displays meaningful sample data.

This helps frontend developers and API consumers understand what information needs to be passed.

---

# 7. Path() – Path Parameter Validation

In the previous section, we learned about Path Parameters.

Now we will learn how to validate them using `Path()`.

### Import

```python
from fastapi import Path
```

### Example

```python
@app.get("/book/{book_id}")
async def read_book(book_id: int = Path(gt=0)):

    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Not Found")
```

### Understanding Path()

```python
book_id: int = Path(gt=0)
```

Here:

- `book_id` is a Path Parameter.
- `int` specifies that the parameter must be an integer.
- `Path()` adds validation rules.
- `gt=0` means the ID must be greater than zero.

### Valid Request

```http
GET http://127.0.0.1:8000/book/1
```

This request is valid because the ID is greater than zero.

### Invalid Request

```http
GET http://127.0.0.1:8000/book/0
```

This request fails validation because the ID must be greater than zero.

FastAPI automatically returns a validation error.

### Key Takeaways

- `Path()` is used to add validation to Path Parameters.
- `gt=0` ensures the ID is positive.
- FastAPI automatically validates the incoming value.
- Invalid values are rejected before the endpoint function executes.

---

# 8. Query() – Query Parameter Validation

In the previous section, we learned how to use Query Parameters for filtering data.

Now we will add validation using `Query()`.

### Import

```python
from fastapi import Query
```

### Example 1: Filter Books by Rating

```python
@app.get("/books")
async def read_book_by_rating(
    book_rating: int = Query(gt=-1, lt=6)
):

    books_to_return = []

    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return
```

### Understanding Query()

```python
book_rating: int = Query(gt=-1, lt=6)
```

- `book_rating` is a Query Parameter.
- `int` specifies the expected data type.
- `Query()` adds validation.
- `gt=-1` means greater than -1.
- `lt=6` means less than 6.

### API Request

```http
GET http://127.0.0.1:8000/books?book_rating=5
```

This returns all books with a rating of 5.

### Example 2: Filter Books by Published Year

```python
@app.get("/books/publish")
async def read_book_by_publish_date(
    published_date: int = Query(gt=1999, lt=2031)
):

    books_to_return = []

    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)

    return books_to_return
```

### API Request

```http
GET http://127.0.0.1:8000/books/publish?published_date=2030
```

This returns books published in 2030.

### Difference Between Path() and Query()

| Path() | Query() |
|---|---|
| Validates Path Parameters | Validates Query Parameters |
| Value is part of the URL path | Value comes after `?` |
| Example: `/book/1` | Example: `/books?book_rating=5` |
| Used to validate resource identifiers | Used to validate filters and other query values |

**Remember:**

- `Path()` → Path Parameter validation.
- `Query()` → Query Parameter validation.
- `Field()` → Pydantic model field validation.

---

# 9. HTTPException – Exception Handling

HTTPException is used to return an HTTP error response when something goes wrong while processing a request.

Import:

```python
from fastapi import HTTPException
```

### Why do we need HTTPException?

Consider this API:

```python
@app.get("/book/{book_id}")
async def read_book(book_id: int = Path(gt=0)):

    for book in BOOKS:
        if book.id == book_id:
            return book
```

What happens if the user requests a book ID that does not exist?

For example:

```http
GET /book/100
```

If no matching book is found, the function returns `None`.

But we want to return a proper HTTP error response.

### Using HTTPException

```python
@app.get("/book/{book_id}")
async def read_book(book_id: int = Path(gt=0)):

    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(
        status_code=404,
        detail="Book Not Found"
    )
```

### Understanding HTTPException

```python
raise HTTPException(
    status_code=404,
    detail="Book Not Found"
)
```

- `raise` stops normal execution and raises an exception.
- `HTTPException` creates an HTTP error response.
- `status_code=404` indicates that the requested resource was not found.
- `detail` provides the error message.

### Expected Response

```json
{
    "detail": "Book Not Found"
}
```

HTTP status:

```text
404 Not Found
```

**Important:** Always use `raise HTTPException(...)`, not just `HTTPException(...)`.

Without `raise`, the exception is created but not actually raised.

---

# 10. HTTP Status Codes

An HTTP Status Code tells the client what happened when the server processed a request.

For example, when a frontend application sends a request to the backend, the backend returns a status code along with its response.

### Why are Status Codes Important?

They help the client understand whether:

- The request was successful.
- A new resource was created.
- The requested resource was not found.
- The request contained invalid data.
- An unexpected server error occurred.

### Importing Status Codes

```python
from starlette import status
```

FastAPI uses Starlette's status constants.

Instead of writing numeric values directly, we can use meaningful constants.

### Common Status Codes Covered in This Section

| Status Code | Meaning | Usage |
|---|---|---|
| 200 | OK | Successful GET request |
| 201 | Created | Resource successfully created |
| 204 | No Content | Request successful, no response body |
| 404 | Not Found | Requested resource does not exist |
| 422 | Unprocessable Entity | Request data failed validation |

### Using Status Codes in FastAPI

**GET API:**

```python
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS
```

**POST API:**

```python
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    pass
```

**PUT API:**

```python
@app.put(
    "/books/update_book",
    status_code=status.HTTP_204_NO_CONTENT
)
async def update_book(book: BookRequest):
    pass
```

**DELETE API:**

```python
@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book(book_id: int):
    pass
```

### Why use status constants instead of numbers?

Instead of:

```python
status_code=200
```

We can write:

```python
status_code=status.HTTP_200_OK
```

This makes the code more readable and easier to understand.

---

# 11. Automatic ID Generation

When creating a new book, we don't want the frontend to generate the ID.

The backend should be responsible for generating unique IDs.

For this learning project, we generate the next ID using the last book's ID.

### Example BOOKS List

```python
BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby',
         'A very nice book!', 5, 2030),

    Book(2, 'Be Fast with FastAPI', 'codingwithroby',
         'A great book!', 5, 2030),

    Book(3, 'Master Endpoints', 'codingwithroby',
         'A awesome book!', 5, 2029)
]
```

### find_book_id() Function

```python
def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book
```

### Understanding the Logic

**1. len(BOOKS)**

Returns the total number of books.

```python
len(BOOKS)
```

If there are 3 books, the result is:

```text
3
```

**2. BOOKS[-1]**

Accesses the last element of the list.

```python
BOOKS[-1]
```

**3. BOOKS[-1].id**

Gets the ID of the last book.

For example:

```text
3
```

**4. BOOKS[-1].id + 1**

Increments the last book ID by one.

```text
3 + 1 = 4
```

**5. book.id = 4**

Assigns the newly generated ID to the new book.

### Shorter Implementation

We can write the same logic using a conditional expression:

```python
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
```

### Important

This ID-generation approach is suitable for learning with an in-memory list.

In real applications, databases generally handle unique ID generation. This list-based approach can also create duplicate IDs if records are deleted and IDs are not sequential.

---

# 12. POST API – Create a New Book with Pydantic

Now we combine Pydantic validation and automatic ID generation.

### Endpoint

```python
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):

    new_book = Book(**book_request.model_dump())

    BOOKS.append(find_book_id(new_book))
```

### Understanding the Implementation

**1. Request Model**

```python
book_request: BookRequest
```

Instead of accepting an unstructured request body, we specify the Pydantic model.

FastAPI automatically validates the incoming JSON against BookRequest.

**2. model_dump()**

```python
book_request.model_dump()
```

Converts the Pydantic model into a Python dictionary.

Example:

```python
{
    "id": None,
    "title": "New Book",
    "author": "Sanjay",
    "description": "Learning FastAPI",
    "rating": 5,
    "published_date": 2025
}
```

**3. Double Asterisk (**)**

```python
Book(**book_request.model_dump())
```

The `**` operator unpacks dictionary key-value pairs as keyword arguments.

Equivalent to:

```python
Book(
    id=None,
    title="New Book",
    author="Sanjay",
    description="Learning FastAPI",
    rating=5,
    published_date=2025
)
```

**4. Automatic ID Generation**

```python
find_book_id(new_book)
```

Generates an ID for the new book.

**5. Append to BOOKS**

```python
BOOKS.append(find_book_id(new_book))
```

Adds the newly created book to the list.

### Example Request

```http
POST http://127.0.0.1:8000/create-book
```

Request Body:

```json
{
    "title": "Python Backend Development",
    "author": "Sanjay",
    "description": "Learning FastAPI and Python",
    "rating": 5,
    "published_date": 2025
}
```

The backend validates the request, generates an ID, and adds the book.

Expected status code:

```text
201 Created
```

---

# 13. PUT API – Update a Book with Validation

PUT is used to update an existing book.

### Endpoint

```python
@app.put(
    "/books/update_book",
    status_code=status.HTTP_204_NO_CONTENT
)
async def update_book(book: BookRequest):

    book_changed = False

    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = Book(**book.model_dump())
            book_changed = True

    if not book_changed:
        raise HTTPException(
            status_code=404,
            detail="Book Not Found"
        )
```

### Understanding the Logic

**1. Receive Updated Book**

```python
book: BookRequest
```

The incoming request is validated using Pydantic.

**2. Initialize a Flag**

```python
book_changed = False
```

This tracks whether an existing book was found and updated.

**3. Iterate Through Books**

```python
for i in range(len(BOOKS)):
```

Iterates through the BOOKS list using indexes.

**4. Find Matching Book**

```python
if BOOKS[i].id == book.id:
```

Checks whether the existing book ID matches the incoming book ID.

**5. Update the Book**

```python
BOOKS[i] = Book(**book.model_dump())
```

Converts the validated Pydantic model into a normal Book object and replaces the existing book.

**6. Update the Flag**

```python
book_changed = True
```

Indicates that the book was successfully updated.

**7. Handle Missing Book**

```python
if not book_changed:
    raise HTTPException(status_code=404, detail="Book Not Found")
```

If no matching book is found, we return a 404 error.

### Example Request

```http
PUT http://127.0.0.1:8000/books/update_book
```

Request Body:

```json
{
    "id": 1,
    "title": "Updated Computer Science",
    "author": "Sanjay",
    "description": "Updated book description",
    "rating": 5,
    "published_date": 2025
}
```

Expected status code:

```text
204 No Content
```

**Important:** Since we use 204, the API should not return a response body.

For this update operation, ID must be provided. Although it is optional in the shared BookRequest model, we should explicitly check for it or create a separate update model with a required ID.

---

# 14. DELETE API – Delete a Book with Validation

DELETE removes a book using its ID.

### Endpoint

```python
@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book(book_id: int = Path(gt=0)):

    book_changed = False

    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break

    if not book_changed:
        raise HTTPException(
            status_code=404,
            detail="Book Not Found"
        )
```

### Understanding the Logic

**1. Path Parameter Validation**

```python
book_id: int = Path(gt=0)
```

Ensures that the book ID is an integer greater than zero.

**2. Initialize Flag**

```python
book_changed = False
```

Tracks whether a matching book was found.

**3. Find the Book**

```python
if BOOKS[i].id == book_id:
```

Checks whether the current book ID matches the requested ID.

**4. Remove the Book**

```python
BOOKS.pop(i)
```

Removes the matching book from the list.

**5. Break**

```python
break
```

Stops the loop once the matching book is deleted.

**6. Handle Missing Book**

```python
if not book_changed:
    raise HTTPException(status_code=404, detail="Book Not Found")
```

Returns a 404 error if the requested book does not exist.

### Example Request

```http
DELETE http://127.0.0.1:8000/books/1
```

Expected status code:

```text
204 No Content
```

If the book ID does not exist:

```json
{
    "detail": "Book Not Found"
}
```

Expected status:

```text
404 Not Found
```

---

# 15. Complete CRUD Operations Summary

| Operation | HTTP Method | Purpose | Status Code |
|---|---|---|---|
| Read all books | GET | Fetch all books | 200 |
| Read book by ID | GET | Fetch a specific book | 200 / 404 |
| Filter by rating | GET | Fetch books by rating | 200 |
| Filter by published year | GET | Fetch books by year | 200 |
| Create book | POST | Create a new book | 201 |
| Update book | PUT | Update an existing book | 204 / 404 |
| Delete book | DELETE | Delete an existing book | 204 / 404 |

---

# 16. Important Corrections in the Original Code

There are a few implementation issues worth understanding.

### 1. find_book_id() Must Return the Book

Original logic:

```python
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
```

Problem: The function does not return anything.

Python functions return `None` by default if there is no explicit return statement.

Therefore:

```python
BOOKS.append(find_book_id(new_book))
```

Would append `None` instead of the book.

Correct implementation:

```python
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
```

### 2. Use raise with HTTPException

Incorrect:

```python
HTTPException(status_code=404, detail="Book Not Found")
```

Correct:

```python
raise HTTPException(
    status_code=404,
    detail="Book Not Found"
)
```

Without `raise`, the exception is not triggered.

### 3. Duplicate GET Endpoint

Your original code defines this endpoint twice:

```python
@app.get("/books")
async def read_book_by_rating(...):
```

The second endpoint has the same HTTP method and path.

Keep only one GET `/books` endpoint. You can use the validated version with Query().

### 4. Convert Pydantic Model to Book Object During Update

Incorrect:

```python
BOOKS[i] = book
```

Here, `book` is a Pydantic model, while the rest of the list contains Book objects.

Correct:

```python
BOOKS[i] = Book(**book.model_dump())
```

This maintains a consistent object type in the list.

### 5. Use model_dump() Instead of dict()

Older Pydantic code:

```python
book_request.dict()
```

Pydantic v2:

```python
book_request.model_dump()
```

`model_dump()` is the recommended method in Pydantic v2.

### 6. ID Should Be Required During Update

Your current BookRequest model makes ID optional.

This is useful when creating a book, but an update operation needs an ID to identify which book to update.

You should validate that ID is present during updates or create separate request models for create and update operations.

---