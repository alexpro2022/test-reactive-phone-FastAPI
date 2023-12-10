from celery.local import PromiseProxy

from app.celery_tasks.tasks import synchronize
from tests.conftest import CURRENCIES
from tests.utils import check_currency


def test_task():
    assert isinstance(synchronize, PromiseProxy), type(synchronize)
    assert synchronize.name == 'app.celery_tasks.tasks.synchronize'
    currencies = synchronize()
    for currency in currencies:
        check_currency(*currency, CURRENCIES)
