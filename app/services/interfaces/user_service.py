from abc import ABC, abstractmethod


class UserServiceInterface(ABC):
    @abstractmethod
    async def create_user(self, username: str):
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int):
        pass

    @abstractmethod
    async def get_all_users(self):
        pass
