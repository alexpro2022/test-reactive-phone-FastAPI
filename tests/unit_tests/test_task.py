from app.celery_tasks.tasks import synchronize


def test_task_name():
    assert synchronize.name == 'app.celery_tasks.tasks.synchronize'
