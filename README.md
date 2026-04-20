# 🔗 AI Workshop — Track Backend

Задание: создать URL-сокращатель как локальное Python-приложение на FastAPI.

## Формат решения

- REST API на Python (FastAPI)
- SQLite (`urls.db` рядом с проектом)
- Локальный запуск без Docker/nginx/compose

## Структура проекта

- `main.py` — точка входа, запуск uvicorn
- `app/` — роуты, модели, сервисы
- `db.py` — работа с SQLite
- `tests/` — тесты
- `requirements.txt` — зависимости (`fastapi`, `uvicorn`)

## Эндпоинты

- `POST /shorten`
- `GET /{code}` (редирект)
- `GET /stats/{code}`
- `GET /health`

## Локальный запуск

```bash
pip install -r requirements.txt && python main.py
```

Сервер должен стартовать на `http://localhost:8000`.

## Проверка

```bash
curl http://localhost:8000/health
bash sample_requests.sh
```

## Advanced (бонус)

1. Добавить middleware логирования в `access.log`:
   - timestamp
   - method
   - path
   - status code
   - response time
2. Добавить `GET /stats/dashboard` с агрегатами:
   - общее количество ссылок
   - общее количество переходов
   - топ-5 самых кликабельных ссылок
   - запросы в минуту за последний час
