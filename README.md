# 🔗 AI Workshop — Track Backend

Задание: создать микросервис URL-сокращатель.

- REST API на Python (FastAPI или Flask)
- SQLite
- Docker
- nginx как reverse proxy

Эндпоинты:
- `POST /shorten`
- `GET /{code}` (302 redirect)
- `GET /stats/{code}`
- `GET /health`

Запуск:

```bash
docker-compose up
```

Бонус: `.github/workflows/ci.yml` с lint, test, docker build.
