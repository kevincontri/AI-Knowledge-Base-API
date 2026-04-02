from app.repositories.interfaces.user_repository import UserRepositoryInterface
from app.repositories.interfaces.note_repository import NoteRepositoryInterface
from app.exceptions.exceptions import NotFoundError
from app.services.interfaces.ai_service import AIServiceInterface

class AIService(AIServiceInterface):
    
    def __init__(self, note_repo: NoteRepositoryInterface, user_repo: UserRepositoryInterface):
        self.note_repo = note_repo
        self.user_repo = user_repo
        
    async def get_user_notes(self, user_id: int):
        if await self.user_repo.get_user_by_id(user_id):
            notes = await self.note_repo.get_user_notes(user_id=user_id)
            return {"notes": notes}
        else:
            raise NotFoundError("User not found")