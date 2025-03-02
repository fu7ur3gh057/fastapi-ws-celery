# 🚀 FastAPI + Celery + PostgreSQL + Redis

## 🔹 Описание
Этот проект использует **FastAPI** для веб-сервиса, **Celery** для фоновых задач, **PostgreSQL** для хранения данных и **Redis** как брокер сообщений для Celery.

---

## 🔹 Перед запуском
Перед запуском необходимо:

   ```sql
   CREATE DATABASE tezt_db;
   ```

после запускаем две команды
```python
python main.py
```

и

```python
celery -A app.scheduler.celery worker --loglevel=info
```