# FastAPI – Books API | Learning Notes

This README covers the fundamentals of FastAPI by building a simple Books API.

The objective is to understand how to:
- Create a FastAPI application.
- Define API endpoints using decorators.
- Run a FastAPI application using Uvicorn.
- Handle GET, POST, PUT, and DELETE requests.
- Work with Path Parameters and Query Parameters.
- Accept request data using Body().
- Perform CRUD operations.
- Explore APIs using Swagger UI.

---

# 1. Introduction to FastAPI

FastAPI is a modern Python web framework used to build REST APIs and backend applications.

It provides:
- High performance.
- Easy API development.
- Automatic request validation.
- Support for asynchronous programming.
- Automatic API documentation using Swagger UI.
- Integration with Python type hints.

### Creating a FastAPI Application

```python
from fastapi import FastAPI

app = FastAPI()
```

**Explanation:**

- `from fastapi import FastAPI`: Imports the FastAPI class.
- `app = FastAPI()`: Creates an instance of the FastAPI application.

The `app` object is responsible for registering API endpoints and handling incoming requests.

### Creating Your First API

```python
@app.get("/")
async def first_api():
    return {"message": "Hello FastAPI"}
```

**Explanation:**

- `@app.get("/")`: Defines a GET endpoint for the root URL.
- `async def`: Defines an asynchronous Python function.
- `first_api()`: Function that handles the incoming request.
- `return`: Sends the response back to the client in JSON format.

**API Request:**

```http
GET http://127.0.0.1:8000/
```

**Expected Response:**

```json
{
    "message": "Hello FastAPI"
}
```

### What is a Decorator?

A decorator is a Python feature that modifies or extends the behavior of a function.

In FastAPI:

```python
@app.get("/")
```

The decorator registers the function as the handler for GET requests to `/`.

Similarly, FastAPI supports different HTTP method decorators:

```python
@app.get("/")
@app.post("/")
@app.put("/")
@app.delete("/")
```

---

# 2. Understanding async and await

FastAPI supports both synchronous and asynchronous functions.

### Asynchronous Function

```python
@app.get("/")
async def first_api():
    return {"message": "Hello FastAPI"}
```

Here, `async` indicates that the function is asynchronous.

### Synchronous Function

```python
@app.get("/")
def first_api():
    return {"message": "Hello FastAPI"}
```

You can also write a FastAPI endpoint without `async`.

**Important points:**

- `async def` is not mandatory for every FastAPI endpoint.
- Use `async def` when working with asynchronous operations.
- Use normal `def` when working with synchronous operations.
- For example, an asynchronous database driver can be used with `await`.

---

# 3. Running the FastAPI Application

There are different ways to start a FastAPI application.

### Using Uvicorn

```bash
uvicorn books:app --reload
```

**Understanding the command:**

| Part | Explanation |
|---|---|
| `uvicorn` | ASGI server used to run the application |
| `books` | Python filename (`books.py`) |
| `app` | FastAPI application instance |
| `--reload` | Automatically restarts the server when code changes |

**Note:** `--reload` is useful during development because you don't need to restart the server manually after every code change.

### Using FastAPI CLI – Development

```bash
fastapi dev books.py
```

Starts the application in development mode.

It provides development-friendly features such as automatic reloading.

### Using FastAPI CLI – Production

```bash
fastapi run books.py
```

Starts the application in production mode.

Unlike development mode, production mode does not enable automatic code reloading by default.

**Quick comparison:**

| Command | Purpose |
|---|---|
| `uvicorn books:app --reload` | Development |
| `fastapi dev books.py` | Development |
| `fastapi run books.py` | Production |

---

# 4. Creating Books Data

For this learning exercise, we are storing books in a Python list instead of using a database.

```python
BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]
```

### Understanding the Data Structure

Here, we are using a combination of:

- **List:** Stores multiple books.
- **Dictionary:** Stores individual book details as key-value pairs.

Example:

```python
{
    'title': 'Title One',
    'author': 'Author One',
    'category': 'science'
}
```

Each dictionary represents one book.

We can access individual values using dictionary keys:

```python
book.get('title')
book.get('author')
book.get('category')
```

### Why are we using a list instead of a database?

For learning purposes, a Python list makes it easy to understand API operations without introducing database concepts.

However, this data is temporary. When the application restarts, changes made to the list are lost.

---

# 5. GET API – Fetch All Books

GET is an HTTP method used to retrieve information from a server.

### Endpoint

```python
@app.get("/books")
async def read_all_books():
    return BOOKS
```

**Explanation:**

- `@app.get("/books")`: Registers a GET endpoint.
- `read_all_books()`: Handles the incoming request.
- `return BOOKS`: Returns all books from the list.

**API Request:**

```http
GET http://127.0.0.1:8000/books
```

**Expected Response:**

```json
[
    {
        "title": "Title One",
        "author": "Author One",
        "category": "science"
    },
    {
        "title": "Title Two",
        "author": "Author Two",
        "category": "science"
    },
    {
        "title": "Title Three",
        "author": "Author Three",
        "category": "history"
    }
]
```

The actual response contains all six books.

### Key Takeaways

- GET is used to retrieve data.
- GET requests generally do not modify server data.
- FastAPI automatically converts Python dictionaries and lists into JSON responses.

---

# 6. Swagger UI – API Documentation

FastAPI automatically generates interactive API documentation.

Once the application is running, open:

```text
http://127.0.0.1:8000/docs
```

This opens Swagger UI.

### What is Swagger UI?

Swagger UI provides an interactive interface to explore and test API endpoints.

You can:
- View all registered endpoints.
- Understand HTTP methods.
- See available request parameters.
- Provide input values.
- Execute API requests.
- View API responses.

For example, you can execute:

```http
GET /books
```

Directly from the Swagger interface without using Postman.

**Important:** FastAPI generates the API documentation automatically using its registered routes, parameter definitions, and request schemas.

---

# 7. Path Parameters

Path Parameters are values passed directly as part of the URL path.

They are generally used to identify a specific resource.

### Example

```python
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
```

### Understanding the Endpoint

```python
@app.get("/books/{book_title}")
```

Here, `{book_title}` is a dynamic path parameter.

FastAPI extracts the value from the URL and passes it to the function argument.

### API Request

```http
GET http://127.0.0.1:8000/books/Title One
```

Here:

```python
book_title = "Title One"
```

FastAPI automatically maps the URL value to the function parameter.

### Understanding the Logic

```python
for book in BOOKS:
    if book.get('title').casefold() == book_title.casefold():
        return book
```

- `for book in BOOKS`: Iterates through every book.
- `book.get('title')`: Retrieves the title of the current book.
- `casefold()`: Performs case-insensitive string comparison.
- If the title matches, the book is returned.

### What is casefold()?

`casefold()` is a Python string method used for case-insensitive string comparisons.

Example:

```python
name1 = "FASTAPI"
name2 = "fastapi"

print(name1.casefold() == name2.casefold())
```

Output:

```text
True
```

It is similar to `lower()` for basic English comparisons, but handles more Unicode case differences.

### Another Example

These requests will match the same book:

```http
GET /books/Title One
GET /books/title one
GET /books/TITLE ONE
```

### Key Takeaways

- Path parameters are defined using `{}`.
- They are extracted directly from the URL.
- FastAPI maps them to function arguments.
- They are useful for identifying specific resources.

---

# 8. Query Parameters

Query Parameters are values passed after the `?` symbol in a URL.

They use a `key=value` format.

They are commonly used for filtering data.

### Example

```python
@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []

    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return
```

### Understanding the Endpoint

```python
@app.get("/books/")
```

This defines the endpoint.

```python
async def read_category_by_query(category: str):
```

Here, `category` is a query parameter.

Because `category` is not part of the URL path, FastAPI treats it as a query parameter.

### API Request

```http
GET http://127.0.0.1:8000/books/?category=science
```

Here:

```python
category = "science"
```

### Understanding the Logic

```python
books_to_return = []
```

Creates an empty list to store matching books.

```python
for book in BOOKS:
```

Iterates through all books.

```python
if book.get('category').casefold() == category.casefold():
```

Checks whether the book category matches the requested category.

```python
books_to_return.append(book)
```

Adds matching books to the result list.

```python
return books_to_return
```

Returns all matching books.

### Expected Response

```json
[
    {
        "title": "Title One",
        "author": "Author One",
        "category": "science"
    },
    {
        "title": "Title Two",
        "author": "Author Two",
        "category": "science"
    }
]
```

### Multiple Query Parameters

FastAPI also supports multiple query parameters.

For example:

```python
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
```

**API Request:**

```http
GET http://127.0.0.1:8000/books/Author Two/?category=math
```

Here:

- `Author Two` is a Path Parameter.
- `category=math` is a Query Parameter.

The API returns books that match both conditions.

**Expected Response:**

```json
[
    {
        "title": "Title Six",
        "author": "Author Two",
        "category": "math"
    }
]
```

---

# 9. Difference Between Path Parameters and Query Parameters

| Path Parameters | Query Parameters |
|---|---|
| Passed as part of the URL path | Passed after `?` |
| Defined using `{}` | Defined as function parameters |
| Generally used to identify resources | Generally used to filter or customize results |
| Usually required when declared in the route | Can be optional |
| `/books/Title One` | `/books?category=science` |

### Example Comparison

**Path Parameter:**

```http
GET /books/Title One
```

Used to retrieve a particular book.

**Query Parameter:**

```http
GET /books?category=science
```

Used to retrieve books belonging to a particular category.

---

# 10. POST API – Create a New Book

POST is an HTTP method used to create new resources on the server.

In FastAPI, we can receive request data using `Body()`.

### Endpoint

```python
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
```

### Understanding Body()

```python
new_book=Body()
```

`Body()` tells FastAPI to read the value from the request body.

The client sends the new book information as JSON.

### Example Request

```http
POST http://127.0.0.1:8000/books/create_book
```

**Request Body:**

```json
{
    "title": "New Book",
    "author": "Sanjay",
    "category": "software"
}
```

### Understanding the Logic

```python
BOOKS.append(new_book)
```

- `append()` is a Python list method.
- It adds the new dictionary to the end of the BOOKS list.

After the request, the new book becomes part of the list.

### Key Takeaways

- POST is generally used to create resources.
- Request data is passed through the request body.
- `Body()` tells FastAPI to read data from the request body.
- `append()` adds a new book to the list.

**Note:** This example uses an untyped request body for simplicity. Later, Pydantic models can be used to validate the incoming book data.

---

# 11. PUT API – Update an Existing Book

PUT is an HTTP method generally used to update an existing resource.

### Endpoint

```python
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            break
```

### Example Request

```http
PUT http://127.0.0.1:8000/books/update_book
```

**Request Body:**

```json
{
    "title": "Title One",
    "author": "Sanjay",
    "category": "technology"
}
```

### Understanding the Logic

```python
for i in range(len(BOOKS)):
```

- `len(BOOKS)` returns the total number of books.
- `range()` generates indexes from `0` to the last index.

```python
if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
```

Checks whether the existing book title matches the title received in the request body.

```python
BOOKS[i] = updated_book
```

Replaces the existing book dictionary with the updated dictionary.

```python
break
```

Stops the loop once the matching book is found and updated.

### Why are we using the index?

We use the index to identify and replace the existing dictionary inside the list.

### Key Takeaways

- PUT is generally used to update a resource.
- The updated information is received through the request body.
- We identify the existing book using its title.
- The matching dictionary is replaced with the updated data.

---

# 12. DELETE API – Delete a Book

DELETE is an HTTP method used to remove an existing resource.

### Endpoint

```python
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
```

### Example Request

```http
DELETE http://127.0.0.1:8000/books/delete_book/Title One
```

### Understanding the Logic

```python
for i in range(len(BOOKS)):
```

Iterates through the list using indexes.

```python
if BOOKS[i].get('title').casefold() == book_title.casefold():
```

Checks whether the current book title matches the requested title.

```python
BOOKS.pop(i)
```

Removes the matching book from the list using its index.

```python
break
```

Stops the loop after deleting the matching book.

### Key Takeaways

- DELETE is used to remove a resource.
- The book title is received as a Path Parameter.
- `pop()` removes an element from the list using its index.

---

# 13. Understanding Python Methods Used in This Project

| Method | Purpose | Example |
|---|---|---|
| `get()` | Retrieves a dictionary value | `book.get('title')` |
| `casefold()` | Converts text for case-insensitive comparison | `"HELLO".casefold()` |
| `append()` | Adds an element to a list | `BOOKS.append(new_book)` |
| `pop()` | Removes an element using its index | `BOOKS.pop(0)` |
| `len()` | Returns the number of elements | `len(BOOKS)` |
| `range()` | Generates a sequence of numbers | `range(len(BOOKS))` |

---

# 14. Important Notes and Improvements

### 1. Duplicate Routes

In the current learning code, `/books/byauthor/` is defined twice.

FastAPI allows route registration, but duplicate paths with the same HTTP method can cause unexpected behavior. Keep only one implementation.

### 2. Route Ordering

The route:

```python
@app.get("/books/{book_title}")
```

can match other single-segment paths under `/books/`.

For example, it can match `/books/byauthor`.

Define specific routes before general dynamic routes where their paths could overlap.

### 3. Missing Book Handling

Currently, if a requested book is not found, the function returns `None`.

Later, you can improve this using FastAPI's `HTTPException` to return a proper 404 response.

### 4. Temporary Data Storage

The BOOKS list is only an in-memory data structure.

It is not a permanent database. Changes are lost when the application restarts.

---

# 15. Interview Questions and Answers

The following questions are based only on the concepts covered in this section.

### Q1. What is FastAPI?

FastAPI is a modern Python web framework used to build REST APIs and backend applications.

It supports automatic validation, asynchronous programming, and automatic API documentation.

### Q2. What is the purpose of `app = FastAPI()`?

It creates an instance of the FastAPI application.

We use this instance to register API endpoints and handle incoming HTTP requests.

### Q3. What is a decorator in FastAPI?

A decorator registers a Python function as an API endpoint.

For example:

```python
@app.get("/")
```

It registers the function to handle GET requests to the root URL.

### Q4. Is async mandatory in FastAPI?

No. FastAPI supports both synchronous (`def`) and asynchronous (`async def`) endpoints.

We use `async def` when working with asynchronous operations.

### Q5. What is Uvicorn?

Uvicorn is an ASGI server used to run FastAPI applications.

It listens for incoming HTTP requests and passes them to the application.

### Q6. What is the difference between `fastapi dev` and `fastapi run`?

- `fastapi dev` starts the application in development mode with automatic reloading.
- `fastapi run` starts the application in production mode without development auto-reloading by default.

### Q7. What are Path Parameters?

Path Parameters are values passed directly through the URL path.

Example:

```http
GET /books/Title One
```

Here, `Title One` is the Path Parameter.

### Q8. What are Query Parameters?

Query Parameters are values passed after the `?` symbol in a URL using key-value pairs.

Example:

```http
GET /books?category=science
```

Here, `category=science` is the Query Parameter.

### Q9. What is the difference between Path Parameters and Query Parameters?

Path Parameters identify a specific resource, whereas Query Parameters are generally used to filter or customize the returned data.

### Q10. How does FastAPI identify whether a parameter is a Path Parameter or Query Parameter?

FastAPI checks the endpoint's route definition.

If the parameter is declared inside `{}` in the route path, it is a Path Parameter.

If it is declared in the function but not in the route path, it is generally treated as a Query Parameter for simple types.

### Q11. What is `casefold()` in Python?

`casefold()` is a string method used for case-insensitive comparisons.

Example:

```python
"FASTAPI".casefold() == "fastapi".casefold()
```

Returns `True`.

### Q12. What is Swagger UI?

Swagger UI is an interactive API documentation interface.

In FastAPI, it is automatically available at:

```text
http://127.0.0.1:8000/docs
```

It allows developers to explore and test API endpoints.

### Q13. What is the difference between GET and POST?

- GET is used to retrieve information.
- POST is generally used to create new resources.

### Q14. What is the purpose of `Body()` in FastAPI?

`Body()` tells FastAPI to read the parameter value from the HTTP request body.

It is commonly used when receiving JSON data from the client.

### Q15. What is the difference between PUT and DELETE?

- PUT is generally used to update an existing resource.
- DELETE is used to remove an existing resource.

### Q16. What is CRUD?

CRUD stands for Create, Read, Update, and Delete.

These represent the four basic operations performed on data.

### Q17. What is the difference between `append()` and `pop()` in Python?

- `append()` adds an element to the end of a list.
- `pop()` removes an element from a list using its index (or removes the last element if no index is supplied).

### Q18. Why are we using `range(len(BOOKS))` in the update and delete APIs?

`len(BOOKS)` gives the total number of books.

`range()` generates the indexes needed to access and modify or remove elements from the list.

---
