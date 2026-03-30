import pytest
from .database import Database

@pytest.mark.asyncio
@pytest.mark.skip(reason="Database connection test")
async def test_database():
    async with Database() as db:
        assert db
        assert db.session