# microservicios-py

Proyecto base en Python con dos contenedores que se comunican por la red `backend` de Docker
usando el **nombre del servicio** (`http://store:6000`), nunca `localhost` ni una IP fija.

```
microservicios-py/
├── api/              # Contenedor 1: Flask (puerto 5000, publicado al host)
│   ├── app/main.py   #   /action/save y /action/list -> reenvía a http://store:6000
│   ├── Dockerfile
│   └── requirements.txt
├── store/            # Contenedor 2: guarda los registros en memoria (puerto 6000, solo red interna)
│   ├── app/main.py
│   ├── Dockerfile
│   └── requirements.txt
├── tests/            # Pruebas con pytest
├── .github/workflows # CI: construye las imágenes en cada push a main
└── docker-compose.yml
```

## Endpoints (api, puerto 5000)

| Método | Ruta | Qué hace |
|---|---|---|
| `POST` | `/action/save` | Guarda el JSON que se envía en el body |
| `GET` | `/action/list` | Lista todo lo guardado |
| `GET` | `/health` | Estado de la api |

## Ejecutar

```bash
docker compose up --build
```

## Probar

Linux / macOS / Git Bash:

```bash
curl -X POST http://localhost:5000/action/save -H "Content-Type: application/json" -d '{"nombre":"Ana","edad":30}'
curl http://localhost:5000/action/list
```

Windows PowerShell (`curl` es un alias de `Invoke-WebRequest` y PowerShell 5.1 quita las
comillas del JSON, por eso se usa `Invoke-RestMethod`):

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:5000/action/save -ContentType 'application/json' -Body '{"nombre":"Ana","edad":30}'
Invoke-RestMethod http://localhost:5000/action/list | ConvertTo-Json -Depth 5
```

> Los datos están en memoria: se pierden al reiniciar el contenedor `store`.

## Pruebas

```bash
pip install flask requests pytest
pytest
```

## Ramas

- `main`: producción
- `dev`: desarrollo
- `qa`: pruebas
