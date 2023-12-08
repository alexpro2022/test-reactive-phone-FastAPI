from celery import Celery

from app.celery_tasks import celeryconfig

app = Celery()
app.config_from_object(celeryconfig)
