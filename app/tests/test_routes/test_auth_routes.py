from app.database import Base, get_db
from app.models import User
from app.tests.utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

# Testing the user registration endpoint
def test_register_user(test_user):
    response = client.post("/auth/register",json={
        "username": "newuser",
        "first_name": "New",
        "last_name": "User",
        "email": "newuser@example.com",
        "password": "newpassword"
    })
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"
    
    # Attempting to register a new user with the same username
    response = client.post("/auth/register", json={
        "username": "newuser",
        "first_name": "Alex",
        "last_name": "Hedges",
        "email": "anotheremail@example.com",
        "password": "differentpassword"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"
    
# Testing the login fro access token endpoint
def test_login_for_access_token(test_user):
    response = client.post("/auth/token", data={
        "username": "alextest",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    
# Attempting to login with invalid credentials
def test_login_for_access_token_invalid_password(test_user):
    response = client.post("/auth/token", data={
        "username": "alextest",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
    
# Testing login with a non-existent user
def test_login_for_access_token_non_existent_user(test_user):
    response = client.post("/auth/token", data={
        "username": "nonexistentuser",
        "password": "somepassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"