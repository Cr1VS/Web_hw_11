from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for declarative models.
    """


class User(Base):
    """
    Model representing users in the database.
    """

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), index=True)
    second_name: Mapped[str] = mapped_column(String(50), index=True)
    phone_num: Mapped[str] = mapped_column(String(25), unique=True, index=True)
    email_add: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    birth_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
