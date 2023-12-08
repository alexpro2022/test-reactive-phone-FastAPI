from app.core import settings

imports = ['app.celery_tasks.tasks']
broker_url = settings.celery_broker_url
beat_schedule = {
    f'synchronize-every-{settings.celery_task_period}-seconds': {
        'task': 'app.celery_tasks.tasks.synchronize',
        'schedule': settings.celery_task_period,
    },
}
timezone = 'Europe/Moscow'
