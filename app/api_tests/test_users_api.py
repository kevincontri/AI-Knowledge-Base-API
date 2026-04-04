from fastapi.testclient import TestClient
from app.server.server import app

client = TestClient(app)


def test_get_all_users():
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert "count" in data

    for user in data["users"]:
        assert "id" in user
        assert "username" in user
        assert "created_at" in user


def test_get_user_by_id():
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data["user"]
    assert "username" in data["user"]
    assert "created_at" in data["user"]
