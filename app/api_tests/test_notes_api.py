from fastapi.testclient import TestClient
from app.server.server import app
from app.core.auth import get_current_user


def override_get_current_user():
    return 1


app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


def test_create_note():
    response = client.post(
        "/notes",
        json={"title": "Test Note", "content": "This is a test note."},
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data["note"]
    assert data["note"]["title"] == "Test Note"
    assert data["note"]["content"] == "This is a test note."
    assert "created_at" in data["note"]
    response = client.delete(f"/notes/{data['note']['id']}")
    assert response.status_code == 204


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
    response = client.get("/notes/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data["note"]
    assert "title" in data["note"]
    assert "content" in data["note"]


def test_update_note():
    response = client.post(
        "/notes",
        json={"title": "Note for update", "content": "This note will be updated."},
    )
    response = client.put(
        f"/notes/{response.json()['note']['id']}",
        json={
            "title": "Updated Note",
            "content": "This is an updated note from a TestClient.",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data["note"]
    assert data["note"]["title"] == "Updated Note"
    assert data["note"]["content"] == "This is an updated note from a TestClient."
    assert "created_at" in data["note"]
    response = client.delete(f"/notes/{data['note']['id']}")
    assert response.status_code == 204


def test_delete_note():
    response = client.post(
        "/notes",
        json={"title": "Note for deletetion", "content": "This note will be deleted."},
    )
    note_id = response.json()["note"]["id"]
    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 204
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 404
