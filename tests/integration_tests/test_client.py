import asyncio
from datetime import datetime as dt
from datetime import timedelta

import pytest

from app.client.deribit import CURRENCIES, get_tickers


@pytest.mark.asyncio
async def test_httpx_client(event_loop):
    assert event_loop is asyncio.get_running_loop()
    # assert asyncio.iscoroutine(get_tickers())
    before = dt.now() - timedelta(seconds=1)
    after = dt.now() + timedelta(minutes=1)
    async for ticker in get_tickers():
        assert ticker.get('result').get('instrument_name').split('-')[0] in CURRENCIES
        assert isinstance(ticker.get('result').get('index_price'), float)
        assert isinstance(ticker.get('result').get('timestamp'), int)
        assert before.timestamp() < ticker.get('result').get('timestamp') / 1000 < after.timestamp()
