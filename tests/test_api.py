import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "api"))

from app.main import app  # noqa: E402


def test_health():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_echo():
    client = app.test_client()
    resp = client.post("/echo", json={"hola": "mundo"})
    assert resp.get_json()["received"] == {"hola": "mundo"}
