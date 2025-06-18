# File for testing utility functions in the app
# This file will contain utility functions for testing purposes.

from sqlalchemy import create_engine, text
from database import Base, sessionmaker
from main import app
from fastapi.testclient import TestClient
import pytest
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
        
client = TestClient(app)

# Override the database dependency in the FastAPI app
app.dependency_overrides[get_db] = override_get_db