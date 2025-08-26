# models/movie.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id"))

    genre = relationship("Genre", back_populates="movies")
    reviews = relationship("Review", back_populates="movie")
