from typing import List

from fastapi import APIRouter, Depends, Query
import httpx
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.utils import get_text_embedding

from src.models.genres import Genre
from src.models.movie import Movie
from src.models.db_helper import db_helper
from src.schemas.movie import MovieResponse, MovieCreate
from src.config import settings
from fastapi import HTTPException
from src.schemas.omdb import OMDBMovie


router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/", response_model=List[MovieResponse])
async def get_movies(db: AsyncSession = Depends(db_helper.session_getter)):
    result = await db.execute(
        select(Movie).options(selectinload(Movie.genres), selectinload(Movie.reviews))
    )

    movies = result.scalars().all()

    return [MovieResponse.model_validate(movie) for movie in movies]


async def fetch_omdb_movie(title: str) -> OMDBMovie:
    title = "+".join(title.lower().split())
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://www.omdbapi.com/?t={title}&apikey={settings.omdb.api_key}"
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=400, detail=response.json().get("Фильм не найден")
            )
        return OMDBMovie(**response.json())


@router.post("/from-omdb", response_model=MovieResponse)
async def add_movie_from_omdb(
    title: str, db: AsyncSession = Depends(db_helper.session_getter)
):
    omdb_data = await fetch_omdb_movie(title)

    movie_data = MovieCreate(
        imdbID=omdb_data.imdbID,
        title=omdb_data.Title,
        year=omdb_data.Year,
        genre_names=omdb_data.Genre.split(", ") if omdb_data.Genre else None,
        plot=omdb_data.Plot,
        director=omdb_data.Director,
    )

    result = await db.execute(select(Movie).where(Movie.imdbID == movie_data.imdbID))
    existing_movie = result.scalars().first()
    if existing_movie:
        raise HTTPException(status_code=400, detail="Такой фильм уже есть")

    db_movie = Movie(
        imdbID=movie_data.imdbID,
        title=movie_data.title,
        year=movie_data.year,
        plot=movie_data.plot,
        director=movie_data.director,
        plot_embedding=get_text_embedding(movie_data.plot),
    )

    if movie_data.genre_names:
        for genre_name in movie_data.genre_names:
            result = await db.execute(
                select(Genre).filter(Genre.name == genre_name.strip())
            )
            genre = result.scalars().first()
            if not genre:
                genre = Genre(name=genre_name.strip())
                db.add(genre)
                await db.flush()
            db_movie.genres.append(genre)

    db.add(db_movie)
    await db.commit()

    result = await db.execute(
        select(Movie)
        .options(selectinload(Movie.genres), selectinload(Movie.reviews))
        .where(Movie.id == db_movie.id)
    )
    db_movie = result.scalars().first()

    return MovieResponse.model_validate(db_movie)


@router.get("/search/plot", response_model=List[MovieResponse])
async def search_movies_by_plot(
    query: str = Query(..., description="поисковой запрос"),
    limit: int = 5,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    query_embedding = get_text_embedding(query)
    stmt = (
        select(Movie)
        .options(
            selectinload(Movie.genres),
            selectinload(Movie.reviews),
        )
        .order_by(Movie.plot_embedding.l2_distance(query_embedding))
        .limit(10)
    )

    resutl = await db.execute(stmt)
    movies = resutl.scalars().all()

    return [MovieResponse.model_validate(movie) for movie in movies]
