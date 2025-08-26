# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file (can be changed to PostgreSQL/MySQL later)
DATABASE_URL = "sqlite:///watchlist.db"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Session factory
SessionLocal = sessionmaker(bind=engine)

# Base class for models
Base = declarative_base()

def init_db():
    """Import models and create tables"""
    import models.user
    import models.movie
    import models.review
    import models.genre
    Base.metadata.create_all(bind=engine)
