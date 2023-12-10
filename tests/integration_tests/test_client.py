import asyncio
from datetime import datetime as dt
from datetime import timedelta

import pytest

from app.client.deribit import CURRENCIES, get_data_from_tickers


@pytest.mark.asyncio
async def test_get_data_from_tickers(event_loop):
    assert event_loop is asyncio.get_running_loop()
    # assert asyncio.iscoroutine(get_data_from_tickers)
    seconds = 10
    data = await get_data_from_tickers()
    for name, price, timestamp in data[0]:
        assert name in CURRENCIES
        assert isinstance(price, float)
        assert isinstance(timestamp, int)
        res = ((dt.now() - timedelta(seconds=seconds)).timestamp() <
               timestamp <
               (dt.now() + timedelta(seconds=seconds)).timestamp())
        assert res
