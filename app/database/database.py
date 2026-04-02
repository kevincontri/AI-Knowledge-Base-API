from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import Optional
from .base import metadata
import asyncio

CONNECTION = "sqlite+aiosqlite:///database.db"

engine = create_async_engine(
    CONNECTION,
    pool_size=2,
    max_overflow=0,
    pool_timeout=30,
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


class Database:
    def __init__(self) -> None:
        self.session: Optional[AsyncSession] = None

    async def __aenter__(self):
        self.session = AsyncSessionLocal()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()


async def init_db():
    from app.models import user, note

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())
