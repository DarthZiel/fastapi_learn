from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from src.models import Review, Movie
from src.schemas.review import ReviewCreate, ReviewResponse
from src.models.db_helper import db_helper

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("/", response_model=ReviewResponse)
async def create_review(
    review: ReviewCreate, db: AsyncSession = Depends(db_helper.session_getter)
):
    result = await db.execute(select(Movie).filter(Movie.id == review.movie_id))
    movie = result.scalars().first()
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")

    db_review = Review(**review.dict())
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return ReviewResponse.model_validate(db_review)


@router.get("/movie/{movie_id}", response_model=List[ReviewResponse])
async def get_reviews_by_movie(
    movie_id: int, db: AsyncSession = Depends(db_helper.session_getter)
):
    result = await db.execute(select(Review).filter(Review.movie_id == movie_id))
    reviews = result.scalars().all()
    return [ReviewResponse.model_validate(review) for review in reviews]
