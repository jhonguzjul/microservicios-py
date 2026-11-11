"""Servicio API (contenedor 1): recibe peticiones y las reenvía al store por su nombre de servicio."""
import os
import socket

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Nombre del servicio en la red de Docker, nunca localhost ni una IP.
STORE_URL = os.getenv("STORE_URL", "http://store:6000")


@app.get("/health")
def health():
    return jsonify(status="ok", service="api", host=socket.gethostname())


@app.post("/items/<key>")
def save_item(key):
    body = request.get_json(silent=True) or {}
    try:
        resp = requests.post(f"{STORE_URL}/data/{key}", json=body, timeout=3)
    except requests.RequestException as exc:
        return jsonify(error=f"store no disponible: {exc}"), 502
    return jsonify(via=STORE_URL, store=resp.json()), resp.status_code


@app.get("/items/<key>")
def read_item(key):
    try:
        resp = requests.get(f"{STORE_URL}/data/{key}", timeout=3)
    except requests.RequestException as exc:
        return jsonify(error=f"store no disponible: {exc}"), 502
    return jsonify(via=STORE_URL, store=resp.json()), resp.status_code


if __name__ == "__main__":
    port = int(os.getenv("API_PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
