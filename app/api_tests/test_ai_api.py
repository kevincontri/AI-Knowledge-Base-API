from fastapi.testclient import TestClient
from app.server.server import app
from app.core.auth import get_current_user

def override_get_current_user():
    return 1

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

def test_ask():
    response = client.post("/ai/ask", json={"prompt": "Test prompt"})
    assert response.status_code == 200
    data = response.json()
    assert "ai_response" in data