import asyncio

from tests import conftest as c


def test_event_loop_fixture(event_loop) -> None:
    # assert event_loop is asyncio.get_running_loop()
    event_loop.run_until_complete(asyncio.sleep(0))


def test_get_test_session(get_test_session) -> None:
    assert isinstance(get_test_session, c.AsyncSession)


@c.pytest_mark_anyio
async def test_get_test_redis(get_test_redis) -> None:
    assert isinstance(get_test_redis, c.FakeRedis)
    assert await get_test_redis.set('key', 'value')
    assert await get_test_redis.get('key') == b'value'
    assert await get_test_redis.set('key', 'value2')
    assert await get_test_redis.get('key') == b'value2'
    assert await get_test_redis.delete('key')
    assert await get_test_redis.get('key') is None


# --- Fixtures for endpoints testing -----------------------------------------------
def test_async_client(async_client) -> None:
    assert isinstance(async_client, c.AsyncClient)


@c.pytest_mark_anyio
async def test_new_post(new_post) -> None:
    assert new_post
