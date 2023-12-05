import asyncio
from typing import Any

import pytest
import pytest_asyncio

from app.repositories.redis_repository import RedisBaseRepository
from tests.base_services.conftest import FakeRedis, pytest_mark_anyio
from tests.utils import compare


class TestBaseRedis:
    prefix = 'prefix:'
    redis: RedisBaseRepository
    time_expire = 1

    @pytest_asyncio.fixture
    async def init(self, get_test_redis: FakeRedis) -> None:
        self.redis = RedisBaseRepository(get_test_redis, self.prefix)

    @pytest_asyncio.fixture
    async def init_expire(self, get_test_redis: FakeRedis) -> None:
        self.redis = RedisBaseRepository(
            get_test_redis, redis_expire=self.time_expire)

    def test_init_fixture(self, init) -> None:
        assert isinstance(self.redis, RedisBaseRepository)

    async def _cache_empty(self):
        return await self.redis.get_all() is None

    @pytest.mark.parametrize('suffix', (1, 1.2, '1', [1, 2], (1, 2), {1, 1, 2}, {'1': 300}))
    def test_get_key(self, init, suffix: Any) -> None:
        key = self.redis._get_key(suffix)
        assert isinstance(key, str)
        assert key == f'{self.prefix}{suffix}'

    @pytest_mark_anyio
    async def test_cache_expire(self, init_expire, get_test_obj) -> None:
        await self.redis.set_all([get_test_obj])
        assert not await self._cache_empty()
        await asyncio.sleep(self.time_expire)
        assert await self._cache_empty()

    @pytest_mark_anyio
    @pytest.mark.parametrize('method_name', ('set_all', 'set_obj'))
    async def test_set_xxx(self, init, get_test_obj, method_name) -> None:
        method = self.redis.__getattribute__(method_name)
        args = [get_test_obj] if method_name == 'set_all' else get_test_obj
        assert await self._cache_empty()
        await method(args)
        assert not await self._cache_empty()

    @pytest_mark_anyio
    async def test_delete_obj(self, init, get_test_obj) -> None:
        await self.redis.set_obj(get_test_obj)
        assert not await self._cache_empty()
        await self.redis.delete_obj(get_test_obj)
        assert await self._cache_empty()

    @pytest_mark_anyio
    @pytest.mark.parametrize('method_name', ('get_all', 'get_obj'))
    async def test_get_xxx_returns_None(self, init, get_test_obj, method_name) -> None:
        method = self.redis.__getattribute__(method_name)
        coro = method() if method_name == 'get_all' else method(1)
        assert await coro is None

    @pytest_mark_anyio
    @pytest.mark.parametrize('method_name', ('get_all', 'get_obj'))
    async def test_get_xxx_returns_obj(self, init, get_test_obj, method_name) -> None:
        await self.redis.set_obj(get_test_obj)
        method = self.redis.__getattribute__(method_name)
        coro = method() if method_name == 'get_all' else method(1)
        result = await coro
        obj = result[0] if isinstance(result, list) else result
        compare(obj, get_test_obj)
