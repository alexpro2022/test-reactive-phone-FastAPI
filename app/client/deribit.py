import asyncio
from typing import Any, Generator
from urllib.parse import urljoin

import httpx

from .utils import load, log

BASE_URL = 'https://test.deribit.com/api/v2/'
TICKER_ENDPOINT = 'public/ticker?instrument_name='
CURRENCIES = ('BTC', 'ETH')
CURRENCIES_PERPETUAL = [item + '-PERPETUAL' for item in CURRENCIES]


async def get_ticker(client, url):
    response = await client.get(url)
    return response.json()


async def get_tickers(currencies: list[str] = CURRENCIES_PERPETUAL) -> Generator[Any, Any, None]:
    url = urljoin(BASE_URL, TICKER_ENDPOINT)
    async with httpx.AsyncClient(http2=True) as client:
        tasks = [get_ticker(client, url + currency)
                 for currency in currencies]
        # return await asyncio.gather(*tasks)
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                yield result


@log
@load
async def get_data_from_tickers() -> Generator[str, float, int]:
    async for ticker in get_tickers():
        name: str = ticker.get('result').get('instrument_name').split('-')[0]
        price: float = ticker.get('result').get('index_price')
        timestamp: int = ticker.get('result').get('timestamp')
        yield name, price, int(timestamp / 1000)
