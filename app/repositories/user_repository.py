from app.database.database import Database
from .interfaces.user_repository import UserRepositoryInterface
from sqlalchemy import insert, select
from app.models.user import User


class UserRepository(UserRepositoryInterface):

    async def create_user(self, username: str, password: str):
        async with Database() as db:
            query = (
                insert(User)
                .values(username=username, password_hash=password)
                .returning(User)
            )
            result = await db.session.execute(query)
            await db.session.commit()
            inserted_user = result.fetchone()
            return dict(inserted_user._mapping)

        return False

    async def get_user_by_id(self, user_id: int):
        async with Database() as db:
            query = select(User).where(User.c.id == user_id)

            result = await db.session.execute(query)
            user = result.one_or_none()
            if user:
                return dict(user._mapping)
            return None

    async def get_all_users(self):
        async with Database() as db:
            query = select(User)
            result = await db.session.execute(query)
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]

        return None

    async def get_user_by_name(self, username: str):
        async with Database() as db:
            query = select(User).where(User.c.username == username).limit(1)

            result = await db.session.execute(query)
            user = result.one_or_none()
            if user:
                return dict(user._mapping)
            return None
