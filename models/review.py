# models/review.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))

    user = relationship("User", back_populates="reviews")
    movie = relationship("Movie", back_populates="reviews")
