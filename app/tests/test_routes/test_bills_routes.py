# Testing the bills routes. 

from app.database import get_db
from app.tests.utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_create_new_bill(test_user):
    response = client.post("/Bills/create",json={
        "title": "newtitle",
        "amount": 15,
        "due_date": "2025-01-01",
        "user_id": test_user.id
    })
    assert response.status_code == 201
    assert response.json()["title"] == "newtitle"
    
def test_get_all_bills(test_bill):
    response = client.get("/Bills/get-all")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
def test_get_all_bills_none():
    response = client.get("/Bills/get-all")
    assert response.status_code == 404
    assert response.json()['detail'] == "No bills found"

def test_get_bill_by_id(test_bill):
    response = client.get(f"/Bills/bill-by-id/{test_bill.id}")
    assert response.status_code == 200
    
    # Checking that the data matches. 
    data = response.json()
    assert data['title'] == "Electric"
    assert data['amount'] == 100
    
def test_get_bill_by_id_none():
    non_exsiting_id = 8888
    response = client.get(f"/Bills/bill-by-id/{non_exsiting_id}")
    assert response.status_code == 404
    
def test_get_bill_per_user(test_user, test_bill):
    response = client.get(f"/Bills/user-bills/{test_user.id}")
    
    assert response.status_code == 200
    
    # make sure the list of bills returned, returns 1
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    
def test_get_bill_per_user_not_found():
    non_user_id = 9995
    response = client.get(f"/Bills/user-bills/{non_user_id}")
    assert response.status_code == 404
    assert response.json()['detail'] == "No bills found for this user"
    
def test_update_bill(test_bill):
    bill_id = test_bill.id 
    
    new_data = {"title": "testbill"}
    
    # Update the bill 
    response = client.put(f"/Bills/update-bill/{bill_id}", json=new_data)
    assert response.status_code == 200
    
    updated_bill = response.json()
    assert updated_bill['title'] == "testbill"
    assert updated_bill['id'] == bill_id
    
def test_update_bill_not_found():
    non_bill_id = 9898
    
    fake_data = {'title': 'No title'}
    
    response = client.put(f"/Bills/update-bill/{non_bill_id}", json=fake_data)
    assert response.status_code == 404
    assert response.json()['detail'] == 'Bill not found'