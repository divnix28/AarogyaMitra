from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat_route_accepts_legacy_frontend_payload():
    response = client.post(
        "/api/v1/chat/message",
        json={
            "sender": "user_123",
            "message": "I have a mild fever"
        },
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert "message" in data
    assert data["action"] in {"ANSWER", "ESCALATE_TO_HUMAN", "ESCALATE"}
