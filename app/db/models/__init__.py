# Define one declarative base here. 
# Importing the individaul models so Base.metadata sees all tables.

from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

# Import models so Alembic sees them.
from .user import User
from .category import Category
from .transaction import Transaction

# Covenient export for Alembic
metadata = Base.metadata