# File for testing utility functions in the app
# This file will contain utility functions for testing purposes.

from sqlalchemy import create_engine, text
from database import Base, sessionmaker
from main import app
from fastapi.testclient import TestClient
from app.auth_utils import get_current_user
from app.models import Users, Bills, Subscriptions
import pytest
from app.utils import bcrypt_context
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
    user = Users(
        username="alextest",
        first_name= "Alex",
        last_name="Hedges",
        email= "ajhedges@email.com",
        hashed_password= bcrypt_context.hash("testpassword"))
        
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()