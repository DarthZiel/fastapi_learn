from src.schemas.review import ReviewResponse
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str | None


class UserCreateResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    username: str
    reviews: list[ReviewResponse] | None = None
    # password: str

    class Config:
        from_attributes = True


UserCreateResponse.model_rebuild()
UserResponse.model_rebuild()
