from celery.local import PromiseProxy

from app.celery_tasks.tasks import synchronize


def test_task():
    assert isinstance(synchronize, PromiseProxy), type(synchronize)
    assert synchronize.name == 'app.celery_tasks.tasks.synchronize'
