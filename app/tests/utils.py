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

# Function used to import test payments against endpoints
# Imported Test user to stop creating users with same credentials clashing.
@pytest.fixture
def test_user_payment(test_user):

    db = TestingSessionLocal()
    
    # Creating some fake payments for testing purposes
    payment1 = Bills(
        title = 'gas',
        amount = 18,
        due_date = '01/01/2025',
        user_id = test_user.id # Link Bill to the user.
    )
    
    # Adding bill to the database to generate ID
    db.add(payment1)
    db.commit()
    db.refresh(payment1)
    
    payment2 = Subscriptions(
        service_name = 'Netflix',
        monthly_cost = 15,
        renewal_date = '01/01/2024',
        user_id = test_user.id # Link Subscription to the user.
    )
    
    db.add_all([payment1, payment2])
    db.commit()
    
    yield {
        'test_user': test_user,
        'bill': payment1
        }
    # Cleanup: Assumes payment tables are cleaned as shown.
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM bills WHERE user_id=:user_id"), {'user_id': test_user.id})
        connection.execute(text("DELETE FROM subscriptions WHERE user_id=:user_id"), {'user_id': test_user.id})
        connection.execute(text("DELETE FROM users WHERE id=:user_id"), {'user_id': test_user.id})
        connection.commit()

# This function cleans the database before running each test to avoid tests colliding.      
@pytest.fixture(autouse=True)
def clean_database():
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM bills"))
        conn.execute(text("DELETE FROM subscriptions"))
        conn.execute(text("DELETE FROM users"))
        conn.commit()
    yield