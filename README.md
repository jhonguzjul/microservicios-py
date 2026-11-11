# microservicios-py

Proyecto base en Python con dos contenedores que se comunican por una red de Docker.

```
microservicios-py/
├── api/              # Servicio Flask (puerto 5000)
│   ├── app/main.py
│   ├── Dockerfile
│   └── requirements.txt
├── worker/           # Cliente que llama a la API cada N segundos
│   ├── app/main.py
│   ├── Dockerfile
│   └── requirements.txt
├── tests/            # Pruebas con pytest
└── docker-compose.yml
```

## Ejecutar

```bash
docker compose up --build
```

- La API queda en http://localhost:5000/health
- El worker llama a `http://api:5000` (nombre del servicio en la red `backend`) y muestra las respuestas en sus logs:

```bash
docker compose logs -f worker
```

## Pruebas

```bash
pip install flask pytest
pytest
```

## Ramas

- `main`: producción
- `dev`: desarrollo
- `qa`: pruebas
