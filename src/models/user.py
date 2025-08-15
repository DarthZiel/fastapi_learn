from enum import unique

from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from src.models.base import Base


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
