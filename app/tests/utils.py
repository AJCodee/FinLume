# File for testing utility functions in the app
# This file will contain utility functions for testing purposes.

from sqlalchemy import create_engine, text
from app.database import Base, sessionmaker
from app.main import app
from fastapi.testclient import TestClient
from app.auth_utils import get_current_user
from app.models import User, Bills, Subscriptions
import pytest
from app.utils import hash_password
from app.database import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

# Creating a new SQLAlchemy engine for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Dependency override for the FastAPI app
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the get_current_user dependency for testing        
def override_get_current_user():
    return {"username": "alextest", "id": 1}
        
client = TestClient(app)

@pytest.fixture
def test_user():
    user = User(
        username="alextest",
        first_name= "Alex",
        last_name="Hedges",
        email= "ajhedges@email.com",
        hashed_password= hash_password("testpassword"))
        
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
        
@pytest.fixture
def test_user_payment():
    user = User(
        username="alextest",
        first_name= "Alex",
        last_name="Hedges",
        email= "ajhedges@email.com",
        hashed_password= hash_password("testpassword"))
        
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    
    # Creating some fake payments for testing purposes
    payment1 = Bills(
        title = 'gas',
        amount = '18',
        due_date = '01/01/2025'
    )
    
    payment2 = Subscriptions(
        service_name = 'Netflix',
        monthly_cost = '15',
        renewal_date = '01/01/2024'
    )
    
    db.add_all([payment1, payment2])
    db.commit()
    
    yield user

    # Cleanup
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM payments WHERE user_id=:user_id"), {'user_id': user.id})
        connection.execute(text("DELETE FROM users WHERE id=:user_id"), {'user_id': user.id})
        connection.commit()