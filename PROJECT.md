# Backend URL Shortener Demo

> [!WARNING]
> Демонстрационное заполнение для проверки автогрейдера.

## Описание
Локальный FastAPI-сервис для сокращения URL со статистикой переходов.

## Стек технологий
- Python 3.11
- FastAPI + Uvicorn
- SQLite

## Структура файлов
- `main.py` — запуск приложения и middleware логирования
- `app/routes.py` — API-роуты
- `app/services.py` — валидация URL и генерация кода
- `db.py` — доступ к SQLite
- `tests/` — базовые smoke-тесты

## Ограничения
- Без Docker/nginx
- Без внешних БД

## Как запустить
```bash
pip install -r requirements.txt
python main.py
bash sample_requests.sh
```
