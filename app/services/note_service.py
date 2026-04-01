from .interfaces.note_service import NoteServiceInterface
from .user_service import UserService
from app.repositories.interfaces.note_repository import NoteRepositoryInterface


class NoteService(NoteServiceInterface):

    def __init__(self, repo: NoteRepositoryInterface, user_service: UserService):
        self.repo = repo
        self.user_service = user_service

    async def create_note(self, title: str, content: str, user_id: int):

        self.__validate_id(user_id)

        if not await self.user_service.get_user_by_id(user_id):
            raise Exception("User not found/Invalid user id")
        if not title or not content:
            raise Exception("Invalid title or content")
        if len(title) < 3 or len(content) < 3:
            raise Exception("Invalid title or content")
        if len(title) > 100 or len(content) > 1000:
            raise Exception("Invalid title or content")

        return await self.repo.create_note(title, content, user_id)

    async def get_note_by_id(self, note_id: int):
        self.__validate_id(note_id)

        note_info = await self.repo.get_note_by_id(note_id)

        if not note_info:
            raise Exception("Note not found/Invalid note id")

        return note_info

    async def get_all_notes(self):
        notes = await self.repo.get_all_notes()
        return notes

    async def update_note(self, note_id: int, title: str = None, content: str = None):
        self.__validate_id(note_id)

        if await self.get_note_by_id(note_id) is False:
            raise Exception("Note not found/Invalid note id")

        note = await self.repo.update_note(note_id, title, content)
        return note

    async def delete_note(self, note_id: int):
        self.__validate_id(note_id)

        if await self.get_note_by_id(note_id) is False:
            return False

        return await self.repo.delete_note(note_id)

    def __validate_id(self, id):
        if not id or id <= 0 or type(id) != int:
            raise Exception("Invalid note id")

        return True


