import os
from pathlib import Path

TEST_DB_FILE = Path(__file__).parent / "test.db"
if TEST_DB_FILE.exists():
    TEST_DB_FILE.unlink()
os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{TEST_DB_FILE.as_posix()}"

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch


@pytest.fixture(scope="session", autouse=True)
def _mock_ollama():
    embed_patch = patch(
        "app.ai_settings.embedding_client.EmbeddingClient.message_embedding",
        new=AsyncMock(return_value=[0.1] * 768),
    )
    ollama_patch = patch(
        "app.ai_settings.ollama_client.OllamaClient.generate",
        new=AsyncMock(return_value={"message": {"content": "Mock AI response"}}),
    )
    embed_patch.start()
    ollama_patch.start()
    yield
    embed_patch.stop()
    ollama_patch.stop()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _init_test_db():
    from app.database.database import init_db, AsyncSessionLocal, engine
    from app.models.user import User
    from app.models.note import Note
    from app.core.security import hash_password
    from sqlalchemy import insert

    await init_db()

    async with AsyncSessionLocal() as session:
        await session.execute(
            insert(User).values(
                id=1,
                username="seed_user",
                password_hash=hash_password("seed_pass"),
            )
        )
        await session.execute(
            insert(Note).values(
                id=1,
                title="Seed Title",
                content="Seed Content",
                user_id=1,
                embedding=[0.1] * 768,
            )
        )
        await session.commit()

    yield

    await engine.dispose()
    if TEST_DB_FILE.exists():
        TEST_DB_FILE.unlink()
