# File for testing utility functions in the app
# This file will contain utility functions for testing purposes.

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.db.models import Base
from app.main import app
from fastapi.testclient import TestClient
from app.core.security import get_current_user
from app.db.models import User
import pytest
from app.utils import hash_password
from app.db.session import get_db

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

# This function cleans the database before running each test to avoid tests colliding.
@pytest.fixture(autouse=True)
def clean_database():
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM users"))
        conn.commit()
    yield
