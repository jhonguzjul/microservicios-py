"""Servicio store (contenedor 2): guarda y devuelve datos clave/valor en memoria."""
import os
import socket

from flask import Flask, jsonify, request

app = Flask(__name__)
_data = {}


@app.get("/health")
def health():
    return jsonify(status="ok", service="store", host=socket.gethostname())


@app.post("/data/<key>")
def save(key):
    body = request.get_json(silent=True) or {}
    if "value" not in body:
        return jsonify(error="falta 'value'"), 400
    _data[key] = body["value"]
    return jsonify(key=key, value=_data[key], saved=True), 201


@app.get("/data/<key>")
def read(key):
    if key not in _data:
        return jsonify(error=f"clave '{key}' no encontrada"), 404
    return jsonify(key=key, value=_data[key], host=socket.gethostname())


if __name__ == "__main__":
    port = int(os.getenv("STORE_PORT", "6000"))
    app.run(host="0.0.0.0", port=port)
