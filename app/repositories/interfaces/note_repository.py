from abc import ABC, abstractmethod


class NoteRepositoryInterface(ABC):
    @abstractmethod
    async def create_note(self, title: str, content: str, user_id: int):
        pass

    @abstractmethod
    async def get_note_from_user(self, note_id: int, user_id: int):
        pass

    @abstractmethod
    async def get_all_notes_from_user(self):
        pass

    @abstractmethod
    async def update_note_from_user(
        self, note_id: int, user_id: int, title: str = None, content: str = None
    ):
        pass

    @abstractmethod
    async def delete_note_from_user(self, note_id: int, user_id: int):
        pass
