import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(service):
    spec = importlib.util.spec_from_file_location(f"{service}_main", ROOT / service / "app" / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.app


def test_api_health():
    resp = _load("api").test_client().get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["service"] == "api"


def test_api_rechaza_json_invalido():
    resp = _load("api").test_client().post("/action/save", data="{malo", content_type="application/json")
    assert resp.status_code == 400


def test_store_save_and_list():
    client = _load("store").test_client()
    assert client.post("/records", json={"nombre": "Ana"}).status_code == 201
    assert client.post("/records", json={"nombre": "Luis"}).status_code == 201
    data = client.get("/records").get_json()
    assert data["total"] == 2
    assert [r["data"]["nombre"] for r in data["records"]] == ["Ana", "Luis"]
