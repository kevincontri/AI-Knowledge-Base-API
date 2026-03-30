from abc import ABC, abstractmethod

class NoteRepositoryInterface(ABC):
    @abstractmethod
    async def create_note(self, title: str, content: str, user_id: int): pass
    
    @abstractmethod
    async def get_note_by_id(self, note_id: int): pass
    
    @abstractmethod
    async def get_all_notes(self): pass
    
    @abstractmethod
    async def update_note(self, note_id: int, title: str = None, content: str = None): pass
    
    @abstractmethod
    async def delete_note(self, note_id: int): pass