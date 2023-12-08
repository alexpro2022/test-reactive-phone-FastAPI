import asyncio

from app.celery_tasks.celery_app import app as celery
from app.client.deribit import get_data_from_tickers


@celery.task
def synchronize():
    return asyncio.get_event_loop().run_until_complete(get_data_from_tickers())
