# microservicios-py

Dos servicios Flask en Docker. `api` reenvía las peticiones a `store` por la red `backend` usando `http://store:6000`.

| Servicio | Puerto | Rutas |
|---|---|---|
| api | 5000 (publicado) | `POST /action/save`, `GET /action/list` |
| store | 6000 (solo red interna) | `POST /records`, `GET /records` |

## Ejecutar

```bash
docker compose up --build
```

## Probar

```bash
curl -X POST http://localhost:5000/action/save -H "Content-Type: application/json" -d '{"nombre":"Ana"}'
curl http://localhost:5000/action/list
```

PowerShell:

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:5000/action/save -ContentType 'application/json' -Body '{"nombre":"Ana"}'
Invoke-RestMethod http://localhost:5000/action/list
```

## Tests

```bash
pip install flask requests pytest
pytest
```
