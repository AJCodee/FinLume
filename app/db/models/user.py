# class for User.
from __future__ import annotations

from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

from . import Base

# This is the User model
class User(Base):
    """ This is the User accounts model. 
    It is a SQLAlchemy model that represents the users table in the database. """
    
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # relationships (Obviously need to create models for these.)
    categories: Mapped[list["Category"]] = relationship(back_populates="owner")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="owner")