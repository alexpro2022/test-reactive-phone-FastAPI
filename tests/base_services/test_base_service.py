import pytest
import pytest_asyncio
from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import RedisBaseRepository
from app.services.services import BaseService
from tests.base_services.conftest import FakeRedis, pytest_mark_anyio
from tests.base_services.data import CRUD, Data, Service
from tests.utils import (check_exception_info, check_exception_info_not_found,
                         compare, compare_lists, get_method)


class TestBaseService(Data):
    msg_not_found = 'Object(s) not found.'
    msg_not_implemented = "Method or function hasn't been implemented yet."
    base_service: BaseService
    service: Service

    @pytest_asyncio.fixture(autouse=True)
    async def init(self, get_test_session: AsyncSession, get_test_redis: FakeRedis) -> None:
        self.base_service = BaseService(CRUD(self.model, get_test_session),
                                        RedisBaseRepository(get_test_redis))

    def test_init_fixture(self) -> None:
        assert isinstance(self.base_service, BaseService)
        assert isinstance(self.base_service.db, CRUD)
        assert isinstance(self.base_service.redis, RedisBaseRepository)

    @pytest_asyncio.fixture()
    async def get_service(self, get_test_session: AsyncSession, get_test_redis: FakeRedis) -> None:
        self.service = Service(CRUD(self.model, get_test_session),
                               RedisBaseRepository(get_test_redis))

    def test_get_service_fixture(self, get_service) -> None:
        assert isinstance(self.service, Service)
        assert isinstance(self.service.db, CRUD)
        assert isinstance(self.service.redis, RedisBaseRepository)

    @pytest_asyncio.fixture
    async def get_obj_in_db(self):
        return await self.base_service.db.create(self.create_schema(**self.post_payload))

    @pytest_mark_anyio
    async def test_get_obj_in_db_fixture(self, get_obj_in_db) -> None:
        assert not await self._db_empty()
        assert await self._cache_empty()

    async def _db_empty(self) -> bool:
        return await self.base_service.db.get_all() is None

    async def _cache_empty(self) -> bool:
        return await self.base_service.redis.get_all() is None

    async def _check_cache_equals_db(self) -> None:
        db = await self.base_service.db.get_all()
        cache = await self.base_service.redis.get_all()
        compare_lists(db, cache)

    @pytest_mark_anyio
    @pytest.mark.parametrize('args', ('single', 'multiple'))
    async def test_set_cache(self, get_test_obj, args):
        args = [get_test_obj] if args == 'multiple' else get_test_obj
        assert await self._cache_empty()
        await self.base_service.set_cache(args)
        assert not await self._cache_empty()

    @pytest_mark_anyio
    @pytest.mark.parametrize('background_tasks', (None, BackgroundTasks()))
    @pytest.mark.parametrize('args', ('single', 'multiple'))
    async def test_add_bg_task_or_execute(self, get_test_obj, background_tasks, args):
        self.base_service.bg_tasks = background_tasks
        args = [get_test_obj] if args == 'multiple' else get_test_obj
        assert await self._cache_empty()
        await self.base_service._add_bg_task_or_execute(self.base_service.set_cache, args)
        if background_tasks is not None:
            # adding the method set_cache to background but cannot run it as it works via DI
            assert await self._cache_empty()
        else:
            # executing the method set_cache without bg_tasks
            assert not await self._cache_empty()

    @pytest_mark_anyio
    async def test__get_returns_obj_from_db_and_setup_cache(self, get_obj_in_db) -> None:
        assert await self._cache_empty()
        objs = await self.base_service._BaseService__get()
        compare(objs[0], get_obj_in_db)
        assert not await self._cache_empty()
        await self._check_cache_equals_db()

    @pytest_mark_anyio
    async def test__get_returns_obj_from_cache(self, get_test_obj) -> None:
        await self.base_service.set_cache(get_test_obj)
        assert await self._db_empty()
        objs = await self.base_service._BaseService__get()
        compare(objs[0], get_test_obj)

    @pytest_mark_anyio
    async def test_get_method(self, get_obj_in_db) -> None:
        """`get` should return None or object."""
        method = self.base_service.get
        assert await method(11) is None
        obj = await method(1)
        compare(obj, get_obj_in_db)

    @pytest_mark_anyio
    async def test_get_or_404_method(self, get_obj_in_db) -> None:
        """`get_or_404` should raise `HTTP_404_NOT_FOUND` or return object."""
        method = self.base_service.get_or_404
        with pytest.raises(HTTPException) as exc_info:
            await method(11)
        check_exception_info_not_found(exc_info, self.msg_not_found)
        obj = await method(1)
        compare(obj, get_obj_in_db)

    @pytest_mark_anyio
    async def test_get_all_method(self) -> None:
        """`get_all` should raise `HTTP_404_NOT_FOUND` or return "None or object."""
        method = self.base_service.get_all
        assert await method() is None
        with pytest.raises(HTTPException) as exc_info:
            await method(exception=True)
        check_exception_info_not_found(exc_info, self.msg_not_found)
        obj = await self.base_service.db.create(self.create_schema(**self.post_payload))
        objs = await method()
        compare(objs[0], obj)

    @pytest_mark_anyio
    @pytest.mark.parametrize('background_tasks', (None, BackgroundTasks()))
    async def test_create_method(self, get_service, background_tasks) -> None:
        self.service.bg_tasks = background_tasks
        assert await self._db_empty()
        assert await self._cache_empty()
        created = await self.service.create(self.create_schema(**self.post_payload))
        assert not await self._db_empty()
        obj = await self.service.db.get_or_404(created.id)
        compare(obj, created)
        if background_tasks is not None:
            assert await self._cache_empty()
        else:
            await self._check_cache_equals_db()

    @pytest_mark_anyio
    @pytest.mark.parametrize('background_tasks', (None, BackgroundTasks()))
    async def test_update_method(self, get_service, get_obj_in_db, background_tasks) -> None:
        self.service.bg_tasks = background_tasks
        created = get_obj_in_db
        obj = await self.service.db.get_or_404(created.id)
        compare(created, obj)
        updated = await self.service.update(created.id, self.update_schema(**self.update_payload))
        obj = await self.service.db.get_or_404(created.id)
        compare(updated, obj)
        if background_tasks is not None:
            assert await self._cache_empty()
        else:
            await self._check_cache_equals_db()

    @pytest_mark_anyio
    async def test_delete_method(self, get_service) -> None:
        created = await self.service.create(self.create_schema(**self.post_payload))
        assert not await self._db_empty()
        assert not await self._cache_empty()
        await self.service.delete(created.id)
        assert await self._db_empty()
        assert await self._cache_empty()

# === Exceptions ===
    @pytest_mark_anyio
    @pytest.mark.parametrize('method_name', ('update', 'delete', 'get_or_404'))
    async def test_method_raises_exception_not_found(self, method_name) -> None:
        pk = 1
        payload = self.update_schema(**self.update_payload)
        args = (pk, payload) if method_name == 'update' else (pk, )
        with pytest.raises(HTTPException) as exc_info:
            await get_method(self.base_service, method_name)(*args)
        check_exception_info_not_found(exc_info, self.msg_not_found)

    @pytest_mark_anyio
    @pytest.mark.parametrize('method_name',
                             ('set_cache_on_create', 'set_cache_on_update',
                              'set_cache_on_delete', 'create', 'update', 'delete')
                             )
    async def test_method_raises_exception_not_implemented(self, method_name, get_obj_in_db) -> None:
        pk = 1
        payload = self.update_schema(**self.update_payload)
        match method_name:
            case 'update':
                args = (pk, payload)
            case 'create':
                args = (payload,)
            case _:
                args = (pk, )
        with pytest.raises(NotImplementedError) as exc_info:
            await get_method(self.base_service, method_name)(*args)
        check_exception_info(exc_info, self.msg_not_implemented)

    @pytest_mark_anyio
    @pytest.mark.parametrize('method_name', ('create', 'update', 'delete'))
    async def test_method_not_raising_exception_not_implemented_from_bg_task(self, method_name, get_obj_in_db) -> None:
        self.base_service.bg_tasks = BackgroundTasks()
        pk = 1
        payload = self.update_schema(**self.update_payload)
        match method_name:
            case 'update':
                args = (pk, payload)
            case 'create':
                args = (payload,)
            case _:
                args = (pk, )
        # cannot run task from background as it works via DI
        await get_method(self.base_service, method_name)(*args)
