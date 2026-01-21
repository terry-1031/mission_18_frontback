from sqlalchemy import String, Date, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    release_date: Mapped[object] = mapped_column(Date, nullable=False)
    director: Mapped[str] = mapped_column(String(100), nullable=False)
    genre: Mapped[str] = mapped_column(String(100), nullable=False)
    poster_url: Mapped[str] = mapped_column(String(500), nullable=False)

    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())
