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

# function used to import a test user to test endpoints
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
    db.refresh(user)
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()

# Fixture for testing bill routes.
@pytest.fixture
def test_bill(test_user):
    bill = Bills(
        title="Electric",
        amount=100,
        due_date="2025-01-01",
        user_id=test_user.id
    )
    
    db = TestingSessionLocal()
    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill

#Fixture for testing subscriptions routes.
@pytest.fixture
def test_subscription(test_user):
    sub = Subscriptions(
        service_name="Netflix",
        monthly_cost=15,
        renewal_date="2025-02-02",
        user_id=test_user.id
    )
    
    db = TestingSessionLocal()
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub


# This function cleans the database before running each test to avoid tests colliding.      
@pytest.fixture(autouse=True)
def clean_database():
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM bills"))
        conn.execute(text("DELETE FROM subscriptions"))
        conn.execute(text("DELETE FROM users"))
        conn.commit()
    yield