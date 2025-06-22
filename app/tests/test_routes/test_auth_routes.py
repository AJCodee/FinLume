from app.database import Base, get_db
from app.models import User
from app.tests.utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

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