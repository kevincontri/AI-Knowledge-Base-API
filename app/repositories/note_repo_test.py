import pytest
from .note_repository import NoteRepository

repo = NoteRepository()


@pytest.mark.asyncio
async def test_create_note():
    response = await repo.create_note(
        "Title Test", "Content Test", 1, ["Test Embedding"]
    )
    assert response
    deleted = await repo.delete_note_from_user(response["id"], 1)
    assert deleted
    note = await repo.get_note_from_user(response["id"], 1)
    assert not note


@pytest.mark.asyncio
async def test_get_note_from_user():
    create_response = await repo.create_note(
        "Title Test", "Content Test", 1, ["Test Embedding"]
    )
    note_response = await repo.get_note_from_user(create_response["id"], 1)
    assert note_response
    deleted = await repo.delete_note_from_user(create_response["id"], 1)
    assert deleted
    note = await repo.get_note_from_user(create_response["id"], 1)
    assert not note


@pytest.mark.asyncio
async def test_note_repository_get_all_notes():
    response = await repo.get_all_notes_from_user(1)
    assert response


@pytest.mark.asyncio
async def test_note_repository_update_note():
    note_created = await repo.create_note(
        "Title Test", "Content Test", 1, ["Test Embedding"]
    )
    response = await repo.update_note_from_user(
        note_created["id"],
        1,
        ["Test Embedding"],
        "Title Test Update",
        "Content Test Update",
    )
    assert response
    deleted = await repo.delete_note_from_user(note_created["id"], 1)
    assert deleted
    note = await repo.get_note_from_user(note_created["id"], 1)
    assert not note


@pytest.mark.asyncio
async def test_note_repository_delete_note():
    note_created = await repo.create_note(
        "Title Test", "Content Test", 1, ["Test Embedding"]
    )
    response = await repo.delete_note_from_user(note_created["id"], 1)
    assert response
