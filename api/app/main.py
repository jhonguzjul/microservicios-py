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


@app.post("/action/save")
def save():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify(error="cuerpo JSON inválido",
                       recibido=request.get_data(as_text=True)), 400
    try:
        resp = requests.post(f"{STORE_URL}/records", json=body, timeout=3)
    except requests.RequestException as exc:
        return jsonify(error=f"store no disponible: {exc}"), 502
    return jsonify(resp.json()), resp.status_code


@app.get("/action/list")
def list_all():
    try:
        resp = requests.get(f"{STORE_URL}/records", timeout=3)
    except requests.RequestException as exc:
        return jsonify(error=f"store no disponible: {exc}"), 502
    return jsonify(resp.json()), resp.status_code


if __name__ == "__main__":
    port = int(os.getenv("API_PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
