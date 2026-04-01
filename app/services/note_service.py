from .interfaces.note_service import NoteServiceInterface
from .user_service import UserService
from app.repositories.interfaces.note_repository import NoteRepositoryInterface
from app.exceptions.exceptions import *

class NoteService(NoteServiceInterface):

    def __init__(self, repo: NoteRepositoryInterface, user_service: UserService):
        self.repo = repo
        self.user_service = user_service

    async def create_note(self, title: str, content: str, user_id: int):
        if not await self.user_service.get_user_by_id(user_id):
            raise NotFoundError("User not found")

        return await self.repo.create_note(title, content, user_id)

    async def get_note_by_id(self, note_id: int):
        note_info = await self.repo.get_note_by_id(note_id)

        if not note_info:
            raise NotFoundError("Note not found")

        return note_info

    async def get_all_notes(self):
        notes = await self.repo.get_all_notes()
        return notes

    async def update_note(self, note_id: int, title: str = None, content: str = None):
        await self.get_note_by_id(note_id)
        note = await self.repo.update_note(note_id, title, content)
        return note

    async def delete_note(self, note_id: int):
        await self.get_note_by_id(note_id)
        await self.repo.delete_note(note_id)



