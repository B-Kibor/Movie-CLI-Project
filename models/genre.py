# models/genre.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False, index=True)

    movies = relationship("Movie", back_populates="genre")

    def __repr__(self):
        return f"<Genre id={self.id} name={self.name!r}>"
