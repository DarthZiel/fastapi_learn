from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    __abstract__=True


    id: Mapped[int] = mapped_column(primary_key=True)