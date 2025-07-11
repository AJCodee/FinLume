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