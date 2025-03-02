from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "scheduler",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.scheduler.tasks"]
)

celery_app.conf.task_routes = {
    "app.scheduler.tasks.send_report": {"queue": "emails"}
}

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)
