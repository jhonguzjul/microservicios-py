import os

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)
STORE_URL = os.getenv("STORE_URL", "http://store:6000")


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.post("/action/save")
def save():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify(error="JSON inválido"), 400
    resp = requests.post(f"{STORE_URL}/records", json=body, timeout=3)
    return resp.json(), resp.status_code


@app.get("/action/list")
def list_records():
    resp = requests.get(f"{STORE_URL}/records", timeout=3)
    return resp.json(), resp.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("API_PORT", "5000")))
