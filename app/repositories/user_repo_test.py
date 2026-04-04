import pytest
from .user_repository import UserRepository

repo = UserRepository()


@pytest.mark.asyncio
async def test_create_user():
    response = await repo.create_user("Test User", "password")
    assert response
    deleted = await repo.delete_test_user(response["id"])
    assert deleted
    user = await repo.get_user_by_id(response["id"])
    assert not user


@pytest.mark.asyncio
async def test_get_user_by_id():
    user = await repo.create_user("Test User", "password")
    response = await repo.get_user_by_id(user["id"])
    assert response
    deleted = await repo.delete_test_user(user["id"])
    assert deleted
    user = await repo.get_user_by_id(user["id"])
    assert not user


@pytest.mark.asyncio
async def test_get_all_users():
    response = await repo.get_all_users()
    assert response


@pytest.mark.asyncio
async def test_get_user_by_name():
    user = await repo.create_user("Test User", "password")
    response = await repo.get_user_by_name(user["username"])
    assert response
    deleted = await repo.delete_test_user(user["id"])
    assert deleted
    user = await repo.get_user_by_id(user["id"])
    assert not user
