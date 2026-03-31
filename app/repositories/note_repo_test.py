import pytest
from .note_repository import NoteRepository

repo = NoteRepository()


@pytest.mark.asyncio
async def test_note_repository_create_note():
    response = await repo.create_note("Title Test", "Content Test", 1)
    assert response


@pytest.mark.asyncio
async def test_note_repository_get_note_by_id():
    response = await repo.get_note_by_id(1)
    assert response
    print("Note:", response)


@pytest.mark.asyncio
async def test_note_repository_get_all_notes():
    response = await repo.get_all_notes()
    assert response


@pytest.mark.asyncio
async def test_note_repository_update_note():
    response = await repo.update_note(1, "Title Test Update", "Content Test Update")
    assert response


@pytest.mark.asyncio
async def test_note_repository_delete_note():
    response = await repo.delete_note(1)
    assert response
