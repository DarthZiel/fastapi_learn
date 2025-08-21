import datetime
from typing import List

from sqlalchemy import DateTime, func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    password: Mapped[str] = mapped_column()
    reviews: Mapped[List["Review"]] = relationship(back_populates="user")
