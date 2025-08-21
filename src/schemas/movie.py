from datetime import datetime
from typing import List
from src.schemas.genre import GenreResponse
from src.schemas.review import ReviewResponse
from pydantic import BaseModel


class MovieCreate(BaseModel):
    imdbID: str
    title: str
    year: str
    genre_names: List[str] | None
    plot: str
    director: str

class MovieResponse(BaseModel):
    id: int
    imdbID: str
    title: str
    year: str
    plot: str
    created_at: datetime
    genres: List[GenreResponse] = []
    reviews: List[ReviewResponse] = []
    director: str
    class Config:
        from_attributes = True


MovieResponse.model_rebuild()
