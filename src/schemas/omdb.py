from pydantic import BaseModel


class OMDBMovie(BaseModel):
    Title: str
    Year: str
    imdbID: str
    Genre: str | None
    Director: str
    Plot: str
