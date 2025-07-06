# Testing user routes / Endpoints

from app.database import get_db
from app.tests.utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

# Testing returning all users
def test_get_all_users(test_user):
    response = client.get("/users/return-users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    
# Testing returning with no users found
def test_get_all_users_none():
    response = client.get("/users/return-users")
    assert response.status_code == 404
    assert response.json()['detail'] == "No users found"
    
# Testing getting a user by ID
def test_get_user_by_id(test_user):
    user_id = test_user.id # get the generated ID after commit
    response = client.get(f"/users/user-by-id/{user_id}")
    assert response.status_code == 200
    data = response.json()
    
    assert data['username'] == test_user.username
    assert data['email'] == test_user.email
    
# Testing getting a user with an ID that doesnt match
def test_get_user_by_id_not_found():
    non_exsisting_user_id = 9999
    response = client.get(F"/users/user-by-id/{non_exsisting_user_id}")
    assert response.status_code == 404
    assert response.json()['detail'] == "User not found"

# Testing getting a user by username
def test_get_user_by_username(test_user):
    username = test_user.username
    response = client.get(f"/users/user-by-username/{username}")
    assert response.status_code == 200
    data = response.json()
    
    assert data['username'] == test_user.username
    
# Testing getting a user by username that doesnt exsist
def test_get_user_by_username_not_found():
    non_exsisting_username = 'testuser'
    response = client.get(f"/users/user-by-username/{non_exsisting_username}")
    assert response.status_code == 404
    assert response.json()['detail'] == "User not found"
    
# Testing returning all payments for a user using ID
def test_get_user_payments(test_user_payment):
    user_id = test_user_payment.id
    response = client.get(f"/users/all-payments/{user_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    
    # verify the contents of payments 
    titles = [p.get('title') for p in data if 'title' in p]
    assert "gas" in titles
    
def test_get_user_payments_not_found():
    non_user_id = 9955
    response = client.get(F"/users/all-payments/{non_user_id}")
    assert response.status_code == 404
    assert response.json()['detail'] == "User not found"
    
def test_update_user(test_user):
    user_id = test_user.id
    
    new_data = {"username": "testalex"}
    
    # Update the user with PUT or PATCH
    response = client.put(f"/users/update-user/{user_id}", json=new_data)
    assert response.status_code == 200 
    
    updated_user = response.json()
    assert updated_user['username'] == "testalex"
    assert updated_user['id'] == user_id # double checking its the same user.