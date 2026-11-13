
BOOK_COLLECTION = "books"


def book_helper(book: dict) -> dict:
    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "author": book["author"],
        "description": book["description"],
        "rating": book["rating"],
        "published_year": book["published_year"]
    }
