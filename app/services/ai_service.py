from app.repositories.interfaces.user_repository import UserRepositoryInterface
from app.repositories.interfaces.note_repository import NoteRepositoryInterface
from app.exceptions.exceptions import NotFoundError
from app.services.interfaces.ai_service import AIServiceInterface
from app.ai_settings.ollama_client import OllamaClient
from app.ai_settings.prompt_enhancer import PROMPT_ENHANCER
from app.schemas.ai_schemas import *

class AIService(AIServiceInterface):
    
    def __init__(self, note_repo: NoteRepositoryInterface, user_repo: UserRepositoryInterface):
        self.note_repo = note_repo
        self.user_repo = user_repo
        
    async def ask(self, user_id: int, prompt: str):
        user_notes = await self.__get_user_notes(user_id)
        enriched_prompt = PROMPT_ENHANCER.format(notes=user_notes, user_prompt=prompt)
        ollama_client = OllamaClient()
        response = await ollama_client.generate(enriched_prompt)
        llm_response = response["message"]["content"]
        
        return PromptResponse(response=llm_response)
        
    async def __get_user_notes(self, user_id: int):
        if await self.user_repo.get_user_by_id(user_id):
            notes = await self.note_repo.get_user_notes(user_id=user_id)
            return notes[:5]
        else:
            raise NotFoundError("User not found")