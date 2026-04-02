from fastapi.testclient import TestClient
from app.server.server import app
import pytest

client = TestClient(app)

def test_create_note():
    response = client.post("/notes", json={"title": "Test Note", "content": "This is a test note.", "user_id": 1})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data["note"]
    assert data["note"]["title"] == "Test Note"
    assert data["note"]["content"] == "This is a test note."
    assert "created_at" in data["note"]
    __delete_note_from_db(data["note"]["id"])
    
def test_get_all_notes():
    response = client.get("/notes")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "notes" in data
    
    for note in data["notes"]:
        assert "id" in note
        assert "title" in note
        assert "content" in note

def test_get_note_by_id():
    response = client.get("/notes/2")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data["note"]
    assert "title" in data["note"]
    assert "content" in data["note"]

def test_update_note():
    response = client.put("/notes/1", json={"title": "Updated Note", "content": "This is an updated note from a TestClient."})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data["note"]
    assert data["note"]["title"] == "Updated Note"
    assert data["note"]["content"] == "This is an updated note from a TestClient."
    assert "created_at" in data["note"]

@pytest.mark.skip(reason="Delete note test")
def test_delete_note():
    response = client.delete("/notes/1")
    assert response.status_code == 204
    
    response = client.get("/notes/1")
    assert response.status_code == 404
    
def __delete_note_from_db(note_id: int):
    client.delete(f"/notes/{note_id}")