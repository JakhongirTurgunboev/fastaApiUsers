from fastapi.testclient import TestClient
from api import main
import json

client = TestClient(main.app)


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


def test_read_user():
    # Test reading a user
    response = client.get("/users/1")  # Assuming user ID 1 exists
    assert response.status_code == 200
    user = response.json()
    # Add assertions to verify the user data
    assert "username" in user
    assert "email" in user


def test_search_user():
    # Test searching for a user
    response = client.get("/users/search?name=test")  # Assuming there's a search endpoint
    assert response.status_code == 200
    users = response.json()
    # Add assertions to verify the search results
    assert len(users) > 0
    for user in users:
        assert "username" in user
        assert "email" in user


def test_update_user():
    # Test updating a user
    user_data = {
        "username": "updateduser",
        "email": "updateduser@example.com"
    }
    response = client.put("/users/1", data=json.dumps(user_data))  # Assuming user ID 1 exists
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["username"] == user_data["username"]
    assert updated_user["email"] == user_data["email"]


def test_delete_user():
    # Test deleting a user
    response = client.delete("/users/1")  # Assuming user ID 1 exists
    assert response.status_code == 200

