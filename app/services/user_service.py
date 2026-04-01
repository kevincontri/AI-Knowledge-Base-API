from .interfaces.user_service import UserServiceInterface
from app.repositories.interfaces.user_repository import UserRepositoryInterface


class UserService(UserServiceInterface):

    def __init__(self, repo: UserRepositoryInterface):
        self.repo = repo

    async def create_user(self, username: str):
        if not username or len(username) > 100 or len(username) < 3:
            raise Exception("Invalid username")

        if await self.__isduplicate(username):
            raise Exception("Username already exists")

        user = await self.repo.create_user(username)

        return user

    async def get_user_by_id(self, user_id: int):
        if not user_id:
            raise Exception("Invalid user id")
        user = await self.repo.get_user_by_id(user_id)
        if not user:
            raise Exception("User not found/Invalid user id")
        return user

    async def get_all_users(self):
        users = await self.repo.get_all_users()
        return users

    async def get_user_by_name(self, username: str):
        if not username or len(username) > 100 or len(username) < 3:
            raise Exception("Invalid username")

        user = await self.repo.get_user_by_name(username)
        if not user:
            raise Exception("User not found/Invalid user id")
        return user

    async def __isduplicate(self, username: str):
        return bool(await self.repo.get_user_by_name(username))