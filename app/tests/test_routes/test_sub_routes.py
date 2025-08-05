from app.database import get_db
from app.tests.utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

# Test for creating a new subscription.
def test_create_new_subscriptions(test_user):
    response = client.post("/Subscription/create",json={
        "service_name": "newservice",
        "monthly_cost": 20,
        "renewal_date": "2025-02-02",
        "user_id": test_user.id
    })
    
    assert response.status_code == 201
    assert response.json()["service_name"] == "newservice"

# Test for retrieving all subscriptions.
def test_get_all_subscriptions(test_subscription):
    response = client.get("/Subscription/get-all")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

# Test for retrieving an empty list of subscriptions.
def test_get_all_subscriptions_none():
    response = client.get("/Subscription/get-all")
    assert response.status_code == 404 
    assert response.json()['detail'] == "No subscriptions found"
    
def test_subscriptions_per_user(test_user, test_subscription):
    response = client.get(f"/Subscription/user-subscriptions/{test_user.id}")
    
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    
def test_subscriptions_per_user_not_found():
    non_user_id = 9998
    response = client.get(f"/Subscription/user-subscriptions/{non_user_id}")
    assert response.status_code == 404
    assert response.json()['detail'] == "No subscriptions found for this user"
    
def test_get_subscription_by_id(test_subscription):
    response = client.get(f"/Subscription/get-by-id/{test_subscription.id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data['service_name'] == "Netflix"
    assert data['monthly_cost'] == 15
    
def test_get_subscription_by_id_not_found():
    non_id = 999
    response = client.get(f"/Subscription/get-by-id/{non_id}")
    
    assert response.status_code == 404
    assert response.json()['detail'] == "Subscription not found"
    
def test_update_subscription(test_subscription):
    sub_id = test_subscription.id
    
    new_data = {"service_name": "newname"}
    
    # Update the bill
    response = client.put(f"/Subscription/update/{sub_id}", json=new_data)
    assert response.status_code == 200
    
    updated_subscription = response.json()
    assert updated_subscription['service_name'] == "newname"
    assert updated_subscription['id'] == sub_id
    
def test_update_subscription_not_found():
    non_sub_id = 555
    
    fake_data = {'service_name': 'noname'}
    
    response = client.put(f"/Subscription/update/{non_sub_id}", json= fake_data)
    assert response.status_code == 404
    assert response.json()['detail'] == "Subscription not found"
    
def test_delete_subscription(test_subscription):
    sub_id = test_subscription.id
    response = client.delete(f"/Subscription/delete/{sub_id}")
    assert response.status_code == 204
    
    # Try and retrieve the deleted Subscription
    response = client.get(f"/Subscription/get-by-id/{sub_id}")
    assert response.status_code == 404
    assert response.json()['detail'] == "Subscription not found"