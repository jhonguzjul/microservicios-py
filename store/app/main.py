import os

from flask import Flask, jsonify, request

app = Flask(__name__)
records = []


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.post("/records")
def save():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify(error="JSON inválido"), 400
    record = {"id": len(records) + 1, "data": body}
    records.append(record)
    return jsonify(saved=True, record=record), 201


@app.get("/records")
def list_records():
    return jsonify(total=len(records), records=records)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("STORE_PORT", "6000")))
