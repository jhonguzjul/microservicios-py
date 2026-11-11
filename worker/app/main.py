"""Servicio worker: llama periódicamente a la API por la red interna de Docker."""
import os
import time

import requests

API_URL = os.getenv("API_URL", "http://api:5000")
INTERVAL = int(os.getenv("WORKER_INTERVAL", "5"))


def main():
    print(f"[worker] conectando con {API_URL} cada {INTERVAL}s", flush=True)
    n = 0
    while True:
        n += 1
        try:
            health = requests.get(f"{API_URL}/health", timeout=3).json()
            echo = requests.post(f"{API_URL}/echo", json={"mensaje": n}, timeout=3).json()
            print(f"[worker] health={health} echo={echo}", flush=True)
        except requests.RequestException as exc:
            print(f"[worker] error al contactar la API: {exc}", flush=True)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
