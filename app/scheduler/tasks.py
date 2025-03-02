from celery.utils.log import get_logger

from app.scheduler.celery import celery_app

logger = get_logger(__name__)


@celery_app.task(name="app.scheduler.worker.send_report")
def send_report(email: str):
    print(f"Report sent to {email}")
    logger.info(f"Report sent to {email}")
    return f"Report successfully sent to {email}"
