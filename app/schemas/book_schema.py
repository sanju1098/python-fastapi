
from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    author: str = Field(min_length=2, max_length=50)
    description: str = Field(min_length=5, max_length=200)
    rating: int = Field(ge=0, le=5)
    published_year: int = Field(ge=2000, le=2030)


class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    description: str
    rating: int
    published_year: int
