FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r requirements.txt

# Ensure Celery is available in PATH
ENV PATH="/root/.local/bin:$PATH"

CMD ["celery", "-A", "app.scheduler.celery.celery_app", "workers", "--loglevel=info"]
