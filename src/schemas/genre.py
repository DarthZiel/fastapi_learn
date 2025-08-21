from pydantic import BaseModel
from typing import List


class GenreCreate(BaseModel):
    name: str


class GenreResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
