import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_app(service):
    spec = importlib.util.spec_from_file_location(f"{service}_main", ROOT / service / "app" / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.app


def test_save_invalid_json():
    resp = load_app("api").test_client().post("/action/save", data="{", content_type="application/json")
    assert resp.status_code == 400


def test_store_save_and_list():
    client = load_app("store").test_client()
    client.post("/records", json={"nombre": "Ana"})
    client.post("/records", json={"nombre": "Luis"})
    data = client.get("/records").get_json()
    assert [r["data"]["nombre"] for r in data["records"]] == ["Ana", "Luis"]
