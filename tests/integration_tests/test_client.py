import pytest

from tests.conftest import CURRENCIES, get_data_from_tickers
from tests.utils import check_currency


@pytest.mark.asyncio
async def test_get_data_from_tickers(event_loop):
    for currency in await get_data_from_tickers():
        check_currency(*currency, CURRENCIES)
