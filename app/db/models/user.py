# class for User.
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
Base = declarative_base()

# This is the User model
class User(Base):
    """ This is the User model. 
    It is a SQLAlchemy model that represents the users table in the database. """
    
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # relationships (Obviously need to create models for these.)
    category: Mapped[list["Category"]] = relationship(back_populates="owner")
    transaction: Mapped[list["Transaction"]] = relationship(back_populates="owner")