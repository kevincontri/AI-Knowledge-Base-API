import pytest
from .user_repository import UserRepository

repo = UserRepository()


@pytest.mark.asyncio
async def test_user_repository_create_user():
    response = await repo.create_user("Test User")
    assert response
    
@pytest.mark.asyncio
async def test_user_repository_get_user():
    response = await repo.get_user(1)
    assert response
    
@pytest.mark.asyncio
async def test_user_repository_get_all_users():
    response = await repo.get_all_users()
    assert response