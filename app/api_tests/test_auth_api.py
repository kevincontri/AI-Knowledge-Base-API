from fastapi.testclient import TestClient
from app.server.server import app
from app.repositories.user_repository import UserRepository
import pytest
from app.core.auth import get_current_user

client = TestClient(app)
user_repo = UserRepository()


@pytest.mark.asyncio
async def test_create_user():
    response = client.post(
        "/auth/register",
        json={"username": "test_username", "password": "test_password"},
    )
    assert response.status_code == 201
    assert "id" in response.json()["user"]
    assert response.json()["user"]["username"] == "test_username"
    assert "created_at" in response.json()["user"]
    deleted = await user_repo.delete_test_user(response.json()["user"]["id"])
    assert deleted
    user = await user_repo.get_user_by_id(response.json()["user"]["id"])
    assert not user


@pytest.mark.asyncio
async def test_login():
    register_response = client.post(
        "/auth/register", json={"username": "username", "password": "user_password"}
    )
    login_response = client.post(
        "/auth/login", json={"username": "username", "password": "user_password"}
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert "token_type" in login_response.json()
    deleted = await user_repo.delete_test_user(register_response.json()["user"]["id"])
    assert deleted
    user = await user_repo.get_user_by_id(register_response.json()["user"]["id"])
    assert not user
