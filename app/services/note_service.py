from .interfaces.note_service import NoteServiceInterface
from .user_service import UserService
from app.repositories.interfaces.note_repository import NoteRepositoryInterface
from app.exceptions.exceptions import *
from app.ai_settings.embedding_client import EmbeddingClient

class NoteService(NoteServiceInterface):

    def __init__(self, repo: NoteRepositoryInterface, user_service: UserService):
        self.repo = repo
        self.user_service = user_service

    async def create_note(self, title: str, content: str, user_id: int):
        if not await self.user_service.get_user_by_id(user_id):
            raise NotFoundError("User not found")

        embed_client = EmbeddingClient()
        
        text = f"{title}. {content}"
        
        embeddings = await embed_client.message_embedding(text)
        
        return await self.repo.create_note(title, content, user_id, embeddings)

    async def get_note_from_user(self, note_id: int, user_id: int):
        note_info = await self.repo.get_note_from_user(note_id, user_id)

        if not note_info:
            raise NotFoundError("Note not found")

        return note_info

    async def get_all_notes_from_user(self, user_id: int):
        notes = await self.repo.get_all_notes_from_user(user_id)
        return notes

    async def update_note_from_user(
        self, note_id: int, user_id: int, title: str = None, content: str = None
    ):  
        
        title_to_embed = ""
        content_to_embed = ""
        
        try:
            note = await self.repo.get_note_from_user(note_id, user_id)
            if not note:
                raise NotFoundError("Note not found")
            title_to_embed += note["title"]
            content_to_embed += note["content"]
        except NotFoundError:
            raise NotFoundError("Note not found")
        
        note_to_embed = "{}. {}"
        
        if title is None:
            note_to_embed.format(title_to_embed, content)
        if content is None:
            note_to_embed.format(title, content_to_embed)
        
        if title is not None and content is not None:
            note_to_embed.format(title, content)
            
        embed_client = EmbeddingClient()
        
        embeddings = await embed_client.message_embedding(note_to_embed)     
        
        note = await self.repo.update_note_from_user(note_id, user_id, embeddings, title, content)
        if not note:
            raise NotFoundError("Note not found")
        return note

    async def delete_note_from_user(self, note_id: int, user_id: int):
        if not await self.repo.delete_note_from_user(note_id, user_id):
            raise NotFoundError("Note not found")
