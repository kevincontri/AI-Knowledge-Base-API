import pytest
from .note_service import NoteService


class NoteRepositoryMock:

    async def create_note(self, title: str, content: str, user_id: int):
        return {
            "id": 1,
            "title": title,
            "content": content,
            "user_id": user_id,
            "created_at": "2023-01-01",
        }

    async def get_note_by_id(self, note_id: int):
        return {
            "id": 1,
            "title": "Title Test",
            "content": "Content Test",
            "user_id": 1,
            "created_at": "2023-01-01",
        }

    async def get_all_notes(self):
        return [
            {
                "id": 1,
                "title": "Title Test",
                "content": "Content Test",
                "user_id": 1,
                "created_at": "2023-01-01",
            }
        ]

    async def update_note(self, note_id: int, title: str = None, content: str = None):
        return {
            "id": 1,
            "title": title,
            "content": content,
            "user_id": 1,
            "created_at": "2023-01-01",
        }

    async def delete_note(self, note_id: int):
        return True


class UserServiceMock:

    async def get_user_by_id(self, user_id: int):
        return {"id": 1, "username": "User Test", "created_at": "2023-01-01"}


note_repo = NoteRepositoryMock()
user_service = UserServiceMock()


@pytest.mark.asyncio
async def test_create_note():
    service = NoteService(note_repo, user_service)
    response = await service.create_note("Title Test", "Content Test", 1)
    assert response


@pytest.mark.asyncio
async def test_get_note_by_id():
    service = NoteService(note_repo, user_service)
    response = await service.get_note_by_id(1)
    assert response


@pytest.mark.asyncio
async def test_get_all_notes():
    service = NoteService(note_repo, user_service)
    response = await service.get_all_notes()
    assert response


@pytest.mark.asyncio
async def test_update_note():
    service = NoteService(note_repo, user_service)
    response = await service.update_note(1, "Title Test Update", "Content Test Update")
    assert response


@pytest.mark.asyncio
async def test_delete_note():
    service = NoteService(note_repo, user_service)
    response = await service.delete_note(1)
    assert response
