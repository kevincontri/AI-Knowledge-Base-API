from app.database.database import Database
from .interfaces.user_repository import UserRepositoryInterface 
from sqlalchemy import insert, select
from app.models.user import User

class UserRepository(UserRepositoryInterface):
    
    async def create_user(self, username: str):
        async with Database() as db:
            query = (
                insert(User).
                values(username=username)
            )
            await db.session.execute(query)
            await db.session.commit()
            return 1
        
        return None
            
    async def get_user(self, user_id: int):
        async with Database() as db:
            query = (
                select(User).
                where(User.c.id == user_id)
            )
            
            result = await db.session.execute(query)
            row = result.fetchone()
            return dict(row._mapping)
        
        return None
        
    async def get_all_users(self):
        async with Database() as db:
            query = (
                select(User)
            )
            result = await db.session.execute(query)
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]
        
        return None