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


def test_store_save_and_read():
    client = _load("store").test_client()
    assert client.post("/data/saludo", json={"value": "hola"}).status_code == 201
    resp = client.get("/data/saludo")
    assert resp.get_json()["value"] == "hola"
    assert client.get("/data/nada").status_code == 404
