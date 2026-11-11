"""Servicio store (contenedor 2): guarda en memoria lo que recibe y lo lista."""
import os
import socket

from flask import Flask, jsonify, request

app = Flask(__name__)
_records = []


@app.get("/health")
def health():
    return jsonify(status="ok", service="store", host=socket.gethostname())


@app.post("/records")
def save():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify(error="cuerpo JSON inválido"), 400
    record = {"id": len(_records) + 1, "data": body}
    _records.append(record)
    return jsonify(saved=True, record=record), 201


@app.get("/records")
def list_all():
    return jsonify(total=len(_records), records=_records)


if __name__ == "__main__":
    port = int(os.getenv("STORE_PORT", "6000"))
    app.run(host="0.0.0.0", port=port)
