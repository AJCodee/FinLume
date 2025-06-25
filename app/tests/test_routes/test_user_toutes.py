# Testing user routes / Endpoints

from app.database import get_db
from app.tests.utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_get_all_users(test_user):
    response = client.get("/users/return-users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    
def test_get_all_users_none():
    response = client.get("/users/return-users")
    assert response.status_code == 404
    assert response.json()['detail'] == "No users found"
    
def test_get_user_by_id(test_user):
    user_id = test_user.id # get the generated ID after commit
    response = client.get(f"/users/user-by-id/{user_id}")
    assert response.status_code == 200
    data = response.json()
    
    assert data['username'] == test_user.username
    assert data['email'] == test_user.email
    
def test_get_user_by_id_not_found():
    non_exsisting_user_id = 9999
    response = client.get(F"/users/user-by-id/{non_exsisting_user_id}")
    assert response.status_code == 404
    assert response.json()['detail'] == "User not found"
