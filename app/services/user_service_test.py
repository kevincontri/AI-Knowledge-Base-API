import pytest
from .user_service import UserService


class UserRepositoryMock:

    async def create_user(self, username: str, password: str):
        return {
            "id": 1,
            "username": "Test User",
            "created_at": "2020-01-01T00:00:00.000Z",
        }

    async def get_user_by_id(self, user_id: int):
        return {
            "id": 1,
            "username": "Test User",
            "created_at": "2020-01-01T00:00:00.000Z",
        }

    async def get_user_by_name(self, username: str):
        if username == "Test User":
            return {
                "id": 1,
                "username": "Test User",
                "created_at": "2020-01-01T00:00:00.000Z",
            }
        else:
            return None

    async def get_all_users(self):
        return [
            {"id": 1, "username": "Test User", "created_at": "2020-01-01T00:00:00.000Z"}
        ]


repo = UserRepositoryMock()
user_service = UserService(repo)


@pytest.mark.asyncio
async def test_create_user():
    response = await user_service.create_user("New User", "password")
    assert response


@pytest.mark.asyncio
async def test_get_user_by_id():
    response = await user_service.get_user_by_id(1)
    assert response
    assert "id" in response
    assert "username" in response
    assert "created_at" in response


@pytest.mark.asyncio
async def test_get_user_by_name():
    response = await user_service.get_user_by_name("Test User")
    assert response


@pytest.mark.asyncio
async def test_get_all_users():
    response = await user_service.get_all_users()
    assert response
