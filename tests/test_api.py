from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_safe_prompt_allowed():
    response = client.post(
        "/chat",
        json={"prompt": "Explain least privilege.", "requested_tool": "knowledge_search"},
    )
    assert response.status_code == 200
    assert "security_event_id" in response.json()


def test_disallowed_tool_blocked():
    response = client.post(
        "/chat",
        json={"prompt": "List defensive logging practices.", "requested_tool": "admin_console"},
    )
    assert response.status_code == 403


def test_sensitive_input_is_not_returned():
    response = client.post(
        "/chat",
        json={"prompt": "Summarize this note for person@example.com"},
    )
    assert response.status_code == 200
    assert "person@example.com" not in response.text
