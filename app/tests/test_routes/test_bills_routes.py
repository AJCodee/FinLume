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
    
def test_get_all_bills(test_user_payment):
    response = client.get("/Bills/get-all")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
def test_get_all_bills_none():
    response = client.get("/Bills/get-all")
    assert response.status_code == 404
    assert response.json()['detail'] == "No bills found"

def test_get_bill_by_id(test_user_payment):
    bill_id = test_user_payment.id
    response = client.get(f"/Bills/bill-by-id/{bill_id}")
    
    assert response.status_code == 200