from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime, Numeric, Index
from sqlalchemy.orm import relationship
from app.db_config import Base
from datetime import datetime

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
    hashed_password = Column(String, nullable=False)
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
    
# SECTION BELOW IS FOR BEGINNING ADDING AI INTO PROJECT.

# New class for dealing with Transactions.
class Transaction(Base):
    """ This is the Transaction model.
    It is a SQLAlachemy model that represents the transactions table in the database. """
    
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    
    
    merchant = Column(String, default="", index=True)
    description = Column(String, default="")
    amount = Column(Numeric(12, 2), nullable=False)   # money: use Decimal in app layer
    posted_at = Column(DateTime, default=datetime.utcnow, index=True)

    # human-accepted label (nullable; AI suggests, user confirms)
    category = Column(String, nullable=True, index=True)

    owner = relationship("User", back_populates="transactions")
    
# Store AI suggestions (history, audit)
class AIPrediction(Base):
    """ This is the AIPrediction model
    It is a SQLAlachemy model that represents the AIPrediction table in the database. """
    
    __tablename__ = "ai_predictions"

    id = Column(Integer, primary_key=True)
    tx_id = Column(Integer, ForeignKey("transactions.id"), index=True, nullable=False)
    model_name = Column(String, default="rules_v1")
    predicted_category = Column(String, nullable=False, index=True)
    confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    transaction = relationship("Transaction")