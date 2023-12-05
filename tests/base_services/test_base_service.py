import pytest
import pytest_asyncio
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import RedisBaseRepository
from app.services.services import BaseService
from tests.base_services.conftest import FakeRedis, pytest_mark_anyio
from tests.base_services.data import CRUD, TestData
from tests.utils import (check_exception_info, compare, compare_lists,
                         get_method)

# pytestmark = pytest_mark_anyio


class TestBaseService(TestData):
    MSG_NOT_IMPLEMENTED = "Method or function hasn't been implemented yet."
    base_service: BaseService

    @pytest_asyncio.fixture
    async def init(self, get_test_session: AsyncSession, get_test_redis: FakeRedis) -> None:
        self.base_service = BaseService(CRUD(self.model, get_test_session),
                                        RedisBaseRepository(get_test_redis))

    def test_init_fixture(self, init) -> None:
        assert isinstance(self.base_service, BaseService)
        assert isinstance(self.base_service.db, CRUD)
        assert isinstance(self.base_service.redis, RedisBaseRepository)

    async def _db_empty(self) -> bool:
        return await self.base_service.db.get_all() is None

    async def _cache_empty(self) -> bool:
        return await self.base_service.redis.get_all() is None

    async def _check_cache_equals_db(self) -> None:
        db = await self.base_service.db.get_all()
        cache = await self.base_service.redis.get_all()
        compare_lists(db, cache)


'''
    @pytest_asyncio.fixture
    async def get_obj_from_db(self, init) -> d.Model:
        obj = await self.base_service.db._save(self.model(**self.post_payload))
        assert not await self._db_empty()
        assert await self._cache_empty()
        return obj

    async def test_set_cache_obj(self, get_obj_from_db: d.Model) -> None:
        assert await self._cache_empty()
        await self.base_service.set_cache(get_obj_from_db)
        assert not await self._cache_empty()
        await self._check_cache_equals_db()

    async def test_set_cache_objs(self, get_obj_from_db: d.Model) -> None:
        assert await self._cache_empty()
        await self.base_service.set_cache([get_obj_from_db])
        assert not await self._cache_empty()
        await self._check_cache_equals_db()

    async def test_get_all_returns_None(self, init) -> None:
        assert await self._cache_empty()
        assert await self.base_service.get_all() is None
        assert await self._cache_empty()

    async def test_get_returns_None(self, get_obj_from_db: d.Model) -> None:
        assert await self._cache_empty()
        assert await self.base_service.get(get_obj_from_db.id + 1) is None
        assert await self._cache_empty()

    async def test_get_or_404_raises_exception(self, get_obj_from_db: d.Model) -> None:
        assert await self._cache_empty()
        with pytest.raises(HTTPException):
            await self.base_service.get_or_404(get_obj_from_db.id + 1)
        assert await self._cache_empty()

    async def test_get_all_fills_cache(self, get_obj_from_db) -> None:
        assert await self._cache_empty()
        objs_db = await self.base_service.get_all()
        assert not await self._cache_empty()
        await self._check_cache_equals_db()
        # below is redandance but kept just in case
        objs_cache = await self.base_service.redis.get_all()
        assert isinstance(objs_db, list)
        assert isinstance(objs_cache, list)
        compare(objs_db[0], get_obj_from_db)
        compare(objs_cache[0], get_obj_from_db)

    @pytest.mark.parametrize('method_name', ('get', 'get_or_404'))
    async def test_get_methods_fill_cache(self, method_name, get_obj_from_db):
        assert await self._cache_empty()
        obj_db = await get_method(self.base_service, method_name)(get_obj_from_db.id)
        assert not await self._cache_empty()
        await self._check_cache_equals_db()
        # below is redandance but kept just in case
        obj_cache = await get_method(self.base_service, method_name)(get_obj_from_db.id)
        compare(obj_db, get_obj_from_db)
        compare(obj_cache, get_obj_from_db)

    @pytest.mark.parametrize('method_name', ('set_cache_create', 'set_cache_update', 'set_cache_delete'))
    async def test_set_cache_xxx_raises_exc(self, init, method_name: str) -> None:
        with pytest.raises(NotImplementedError) as exc_info:
            await get_method(self.base_service, method_name)(None)
        check_exception_info(exc_info, "Method or function hasn't been implemented yet.")

    async def test_create_creates_obj_and_raises_exc(self, init) -> None:
        assert await self._db_empty()
        assert await self._cache_empty()
        with pytest.raises(NotImplementedError) as exc_info:
            await self.base_service.create(self.schema(**self.post_payload))
        check_exception_info(exc_info, self.MSG_NOT_IMPLEMENTED)
        assert not await self._db_empty()
        assert await self._cache_empty()

    async def test_update_updates_obj_and_raises_exc(self, get_obj_from_db: d.Model) -> None:
        assert not await self._db_empty()
        assert await self._cache_empty()
        with pytest.raises(NotImplementedError) as exc_info:
            await self.base_service.update(get_obj_from_db.id, self.schema(**self.update_payload))
        check_exception_info(exc_info, self.MSG_NOT_IMPLEMENTED)
        assert not await self._db_empty()
        assert await self._cache_empty()

    async def test_delete_deletes_obj_and_raises_exc(self, get_obj_from_db: d.Model) -> None:
        assert not await self._db_empty()
        assert await self._cache_empty()
        with pytest.raises(NotImplementedError) as exc_info:
            await self.base_service.delete(get_obj_from_db.id)
        check_exception_info(exc_info, self.MSG_NOT_IMPLEMENTED)
        assert await self._db_empty()
        assert await self._cache_empty()



    model = d.Model
    schema = d.Schema
    post_payload = {'title': 'My object', 'description': 'My object description'}
    update_payload = {'title': 'My updated object', 'description': 'My updated object description'}
'''
