# Define one declarative base here. 
# Importing the individaul models so Base.metadata sees all tables.

from sqlalchemy.orm import declarative_base
Base = declarative_base()

from .user import User
from .category import Category
from .transaction import Transaction

# Covenient export for Alembic
metadata = Base.metadata