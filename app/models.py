from sqlalchemy import Column, Integer, String
from database import Base

# This is the User model
class User(Base):
    """ This is the User model. 
    It is a SQLAlchemy model that represents the users table in the database. """
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hased_password = Column(String)