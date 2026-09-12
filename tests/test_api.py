from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz():
    assert client.get("/healthz").json()["status"] == "ok"


def test_version_reports_model_and_prompt_version():
    body = client.get("/version").json()
    assert body["prompt_version"] == "v1"
    assert body["model"]


def test_chat():
    body = client.post("/chat", json={"message": "book a flight to Tokyo"}).json()
    assert body["intent"] == "flight"
    assert body["reply"]


def test_chat_rejects_empty_body():
    assert client.post("/chat", json={}).status_code == 422
