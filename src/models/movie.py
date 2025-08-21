import datetime
from typing import List

from src.models.base import Base
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Movie(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    imdbID: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column()
    year: Mapped[str] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    reviews: Mapped[List["Review"]] = relationship(back_populates="movie")

    genres: Mapped[List["Genre"]] = relationship(
        "Genre", secondary="movie_genres", back_populates="movies"
    )
