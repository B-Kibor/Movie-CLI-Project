# models/__init__.py
from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .user import User  
from .genre import Genre  
from .movie import Movie  
from .review import Review 
