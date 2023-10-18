from fastapi.testclient import TestClient
from api.main import app
import json

client = TestClient(app)


def test_create_user():
    # Test creating a user
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    response = client.post("/users/", data=json.dumps(user_data))

    assert response.status_code == 200
    created_user = response.json()
    assert created_user["username"] == user_data["username"]
    assert created_user["email"] == user_data["email"]
    # Add more assertions as needed


def test_read_user():
    # Test reading a user
    response = client.get("/users/1")  # Assuming user ID 1 exists
    assert response.status_code == 200
    user = response.json()
    # Add assertions to verify the user data
    assert "username" in user
    assert "email" in user
    # Add more assertions as needed