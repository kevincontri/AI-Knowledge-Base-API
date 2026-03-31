import pytest
from .database import Database


@pytest.mark.asyncio
async def test_database():
    async with Database() as db:
        assert db
