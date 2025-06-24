import json
from app import app

def test_identify_new_user():
    client = app.test_client()

    payload = {
        "email": "newuser@test.com",
        "phoneNumber": "1234567890"
    }

    response = client.post('/identify', json=payload)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["primaryContactId"]
    assert "newuser@test.com" in data["emails"]
    assert "1234567890" in data["phoneNumbers"]
