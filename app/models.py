from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# This is the User model
class User(Base):
    """ This is the User model. 
    It is a SQLAlchemy model that represents the users table in the database. """
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hased_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    bills = relationship("Bills", back_populates="owner")
    subscriptions = relationship("Subscriptions", back_populates="owner")
    
class Bills(Base):
    """ This is the Bills model. 
    It is a SQLAlchemy model that represents the bills table in the database. """
    
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    due_date = Column(String, nullable=False)
    
    
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="bills")
    
class Subscriptions(Base):
    """ This is the Subscriptions model. 
    It is a SQLAlchemy model that represents the subscriptions table in the database. """
    
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, nullable=False)
    monthly_cost = Column(Integer, nullable=False) # Could change to consider decimals ?
    renewal_date = Column(String, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="subscriptions")