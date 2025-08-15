from sqlalchemy.orm import Mapped, mapped_column


from src.models.base import Base


class User(Base):
    __tablename__ = "User"
    username: Mapped[str] = mapped_column(unique=True)
