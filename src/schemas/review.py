from pydantic import BaseModel
from datetime import datetime


class ReviewCreate(BaseModel):
    text: str
    rating: int
    movie_id: int
    user_id: int


class ReviewResponse(BaseModel):
    id: int
    text: str
    rating: int
    created_at: datetime
    user_id: int
    movie_id: int

    class Config:
        from_attributes = True


ReviewResponse.model_rebuild()
