"""Servicio API: expone endpoints HTTP que el worker consume."""
import os
import socket

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(status="ok", service="api", host=socket.gethostname())


@app.post("/echo")
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify(received=data, service="api")


if __name__ == "__main__":
    port = int(os.getenv("API_PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
