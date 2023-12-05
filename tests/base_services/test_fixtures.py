import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from tests.base_services.conftest import (Base, FakeRedis, TestData,
                                          pytest_mark_anyio)


def test_event_loop_fixture(event_loop) -> None:
    event_loop.run_until_complete(asyncio.sleep(0))


def test_get_test_session(get_test_session: AsyncSession) -> None:
    assert isinstance(get_test_session, AsyncSession)


@pytest_mark_anyio
async def test_get_test_redis(get_test_redis: FakeRedis) -> None:
    assert isinstance(get_test_redis, FakeRedis)
    assert await get_test_redis.set('key', 'value')
    assert await get_test_redis.get('key') == b'value'
    assert await get_test_redis.set('key', 'value2')
    assert await get_test_redis.get('key') == b'value2'
    assert await get_test_redis.delete('key')
    assert await get_test_redis.get('key') is None


def test_get_test_obj(get_test_obj: TestData.model) -> None:
    assert isinstance(get_test_obj, TestData.model)
    assert get_test_obj.id == 1
    assert get_test_obj.title == TestData.post_payload['title']
    assert get_test_obj.description == TestData.post_payload['description']
