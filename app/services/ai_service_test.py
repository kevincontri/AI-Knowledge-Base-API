import pytest
from .ai_service import AIService


class NoteRepositoryMock:
    async def create_note(
        self, title: str, content: str, user_id: int, embeddings: list
    ):
        return {
            "id": 1,
            "title": title,
            "content": content,
            "user_id": user_id,
            "created_at": "2023-01-01",
            "embedding": ["Test Embedding"],
        }

    async def get_note_from_user(self, note_id: int, user_id: int):
        return {
            "id": note_id,
            "title": "Title Test",
            "content": "Content Test",
            "user_id": user_id,
            "created_at": "2023-01-01",
        }

    async def get_all_notes_from_user(self, user_id: int):
        return [
            {
                "id": 1,
                "title": "Title Test",
                "content": "Content Test",
                "user_id": user_id,
                "created_at": "2023-01-01",
            }
        ]

    async def update_note_from_user(
        self,
        note_id: int,
        user_id: int,
        embeddings: list,
        title: str = None,
        content: str = None,
    ):
        return {
            "id": 1,
            "title": title,
            "content": content,
            "user_id": 1,
            "created_at": "2023-01-01",
        }

    async def delete_note_from_user(self, note_id: int, user_id: int):
        return True

    async def get_user_notes(self, user_id: int):
        return [
            {
                "id": 1,
                "title": "Title Test",
                "content": "Content Test",
                "user_id": user_id,
                "created_at": "2023-01-01",
            }
        ]


class UserRepositoryMock:

    async def create_user(self, username: str, password: str):
        return {
            "id": 1,
            "username": "Test User",
            "created_at": "2020-01-01T00:00:00.000Z",
        }

    async def get_user_by_id(self, user_id: int):
        return {
            "id": user_id,
            "username": "Test User",
            "created_at": "2020-01-01T00:00:00.000Z",
        }

    async def get_all_users(self):
        return [
            {"id": 1, "username": "Test User", "created_at": "2020-01-01T00:00:00.000Z"}
        ]

    async def get_user_by_name(self, username: str):
        return {
            "id": 1,
            "username": "Test User",
            "created_at": "2020-01-01T00:00:00.000Z",
        }


ai_service = AIService(NoteRepositoryMock(), UserRepositoryMock())


@pytest.mark.asyncio
async def test_ask():
    result = await ai_service.ask(user_id=1, prompt="Test Prompt")
    assert result
    assert result.ai_response
