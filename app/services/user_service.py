from .interfaces.user_service import UserServiceInterface
from app.repositories.interfaces.user_repository import UserRepositoryInterface
from app.exceptions.exceptions import *

class UserService(UserServiceInterface):

    def __init__(self, repo: UserRepositoryInterface):
        self.repo = repo

    async def create_user(self, username: str):
        if await self.__isduplicate(username):
            raise DuplicateError("Username already exists")

        user = await self.repo.create_user(username)

        return user

    async def get_user_by_id(self, user_id: int):
        user = await self.repo.get_user_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    async def get_all_users(self):
        users = await self.repo.get_all_users()
        return users

    async def get_user_by_name(self, username: str):
        user = await self.repo.get_user_by_name(username)
        if not user:
            raise NotFoundError("User not found")
        return user

    async def __isduplicate(self, username: str):
        return bool(await self.repo.get_user_by_name(username))