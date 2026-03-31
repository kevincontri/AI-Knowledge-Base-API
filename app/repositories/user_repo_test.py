import pytest
from .user_repository import UserRepository

repo = UserRepository()


@pytest.mark.asyncio
async def test_user_repository_create_user():
    response = await repo.create_user("Test User")
    assert response
    print("User Created:", response)


@pytest.mark.asyncio
async def test_user_repository_get_user_by_id():
    response = await repo.get_user_by_id(1)
    assert response
    print("Username:", response)


@pytest.mark.asyncio
async def test_user_repository_get_all_users():
    response = await repo.get_all_users()
    assert response
    print("Users:", response)


@pytest.mark.asyncio
async def test_user_repository_get_user_by_name():
    response = await repo.get_user_by_name("Test User")
    assert response
    print("Username:", response)
