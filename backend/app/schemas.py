from datetime import date, datetime
from pydantic import BaseModel, HttpUrl, Field

class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    release_date: date
    director: str = Field(min_length=1, max_length=100)
    genre: str = Field(min_length=1, max_length=100)
    poster_url: HttpUrl

class MovieOut(BaseModel):
    id: int
    title: str
    release_date: date
    director: str
    genre: str
    poster_url: str
    created_at: datetime | None = None

    avg_rating: float | None = None

    class Config:
        from_attributes = True
