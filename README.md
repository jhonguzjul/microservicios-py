# microservicios-py

Proyecto base en Python con dos contenedores que se comunican por la red `backend` de Docker
usando el **nombre del servicio** (`http://store:6000`), nunca `localhost` ni una IP fija.

```
microservicios-py/
├── api/              # Contenedor 1: Flask (puerto 5000, publicado al host)
│   ├── app/main.py   #   reenvía /items/<clave> a http://store:6000
│   ├── Dockerfile
│   └── requirements.txt
├── store/            # Contenedor 2: almacén clave/valor (puerto 6000, solo red interna)
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

## Probar la ida y vuelta (api → store → api)

Linux / macOS / Git Bash:

```bash
curl -X POST http://localhost:5000/items/saludo -H "Content-Type: application/json" -d '{"value":"hola"}'
curl http://localhost:5000/items/saludo
```

Windows PowerShell (`curl` es un alias de `Invoke-WebRequest` y PowerShell 5.1 quita las
comillas del JSON, por eso se usa `Invoke-RestMethod`):

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:5000/items/saludo -ContentType 'application/json' -Body '{"value":"hola"}'
Invoke-RestMethod http://localhost:5000/items/saludo
```

O con `curl.exe` escapando las comillas:

```powershell
curl.exe -X POST http://localhost:5000/items/saludo -H "Content-Type: application/json" -d '{\"value\":\"hola\"}'
```

> Leer una clave antes de guardarla devuelve `404` (es lo esperado).

## Pruebas

```bash
pip install flask requests pytest
pytest
```

## Ramas

- `main`: producción
- `dev`: desarrollo
- `qa`: pruebas
