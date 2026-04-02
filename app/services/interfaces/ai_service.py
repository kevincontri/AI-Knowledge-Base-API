from abc import ABC, abstractmethod


class AIServiceInterface(ABC):

    @abstractmethod
    async def ask(self, user_id: int, prompt: str):
        pass

    async def __get_user_notes(self, user_id: int):
        pass
