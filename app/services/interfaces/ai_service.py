from abc import ABC, abstractmethod

class AIServiceInterface(ABC):
    
    @abstractmethod
    async def get_user_notes(self, user_id: int):
        pass