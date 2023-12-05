from typing import Any

import pytest
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import CRUDBaseRepository
from tests.base_services.conftest import pytest_mark_anyio
from tests.base_services.data import CRUD, TestData, TestModel
from tests.utils import (check_exception_info, check_exception_info_not_found,
                         get_method)


class TestCRUDBaseRepository(TestData):
    """Тестовый класс для тестирования базового CRUD класса."""
    msg_already_exists = 'Object with such a unique values already exists.'
    msg_not_found = 'Object(s) not found.'
    # base crud with not implemented hooks
    crud_base_not_implemented: CRUDBaseRepository
    # base crud with implemented hooks
    crud_base_implemented: CRUD

    @pytest.fixture(autouse=True)
    def init(self, get_test_session: AsyncSession) -> None:
        self.crud_base_not_implemented = CRUDBaseRepository(self.model, get_test_session)
        self.crud_base_implemented = CRUD(self.model, get_test_session)

    def test_init_fixture(self):
        assert isinstance(self.crud_base_not_implemented, CRUDBaseRepository)
        assert not isinstance(self.crud_base_not_implemented, CRUD)
        assert isinstance(self.crud_base_implemented, CRUD)

    async def _db_empty(self):
        return await self.crud_base_not_implemented.get_all() is None

    async def _create_object(self) -> TestModel:
        return await self.crud_base_not_implemented._save(self.model(**self.post_payload))

    def _check_obj(self, obj: TestModel, after_create: bool = True) -> None:
        assert isinstance(obj, self.model)
        for field_name in self.field_names:
            assert getattr(obj, field_name)
        payload = self.post_payload if after_create else self.update_payload
        self._compare_values(obj, payload)

    def _compare_values(self, obj: TestModel, payload: dict[str, str]) -> None:
        assert obj.title == payload['title'], (obj.title, payload['title'])
        assert obj.description == payload['description'], (obj.description, payload['description'])

# === CRUD ===
    @pytest_mark_anyio
    async def test_save(self) -> None:
        assert await self._db_empty()
        obj = await self._create_object()
        assert not await self._db_empty()
        self._check_obj(obj)

    @pytest_mark_anyio
    @pytest.mark.parametrize('method_name', ('_get_all_by_attrs', '_get_by_attrs'))
    async def test_get_by_methods(self, method_name: str) -> None:
        title = self.post_payload['title']
        method = get_method(self.crud_base_not_implemented, method_name)
        # returns None if NOT_FOUND and exception=False by default
        assert await method(title=title) is None
        # raises HTTPException if NOT_FOUND and exception=True
        with pytest.raises(HTTPException) as exc_info:
            await method(title=title, exception=True)
        check_exception_info_not_found(exc_info, self.msg_not_found)
        # returns list of objects or object if FOUND
        await self._create_object()
        result = await method(title=title)
        obj = result[0] if method_name == '_get_all_by_attrs' else result
        self._check_obj(obj)

    @pytest_mark_anyio
    async def test_get(self) -> None:
        """`get` should return None or object."""
        assert await self.crud_base_not_implemented.get(1) is None
        await self._create_object()
        obj = await self.crud_base_not_implemented.get(1)
        self._check_obj(obj)

    @pytest_mark_anyio
    async def test_get_or_404(self) -> None:
        """`get_or_404` should raise `HTTP_404_NOT_FOUND` or return object."""
        with pytest.raises(HTTPException) as exc_info:
            await self.crud_base_not_implemented.get_or_404(1)
        check_exception_info_not_found(exc_info, self.msg_not_found)
        await self._create_object()
        obj = await self.crud_base_not_implemented.get_or_404(1)
        self._check_obj(obj)

    @pytest_mark_anyio
    async def test_get_all(self) -> None:
        """`get_all` should raise `HTTP_404_NOT_FOUND` or return "None or object."""
        method = self.crud_base_not_implemented.get_all
        assert await method() is None
        with pytest.raises(HTTPException) as exc_info:
            await method(exception=True)
        check_exception_info_not_found(exc_info, self.msg_not_found)
        await self._create_object()
        objs = await method()
        self._check_obj(objs[0])

    @pytest_mark_anyio
    async def test_create_method(self) -> None:
        assert await self._db_empty()
        obj = await self.crud_base_not_implemented.create(self.create_schema(**self.post_payload))
        assert not await self._db_empty()
        created = await self.crud_base_not_implemented.get_or_404(obj.id)
        self._check_obj(created)

    @pytest_mark_anyio
    async def test_update_method(self) -> None:
        obj = await self._create_object()
        self._check_obj(obj)
        await self.crud_base_implemented.update(obj.id, self.update_schema(**self.update_payload))
        updated = await self.crud_base_not_implemented.get_or_404(obj.id)
        self._check_obj(updated, after_create=False)

    @pytest_mark_anyio
    async def test_delete_method(self) -> None:
        obj = await self._create_object()
        assert not await self._db_empty()
        await self.crud_base_implemented.delete(obj.id)
        assert await self._db_empty()

# === Exceptions ===
    @pytest_mark_anyio
    async def test_save_raise_exception_on_unique(self) -> None:
        await self._create_object()
        with pytest.raises(HTTPException) as exc_info:
            await self._create_object()
        check_exception_info(exc_info, self.msg_already_exists, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.parametrize('method_name, args, expected_msg', (
        ('has_permission', (None, None), 'has_permission() must be implemented.'),
        ('is_update_allowed', (None, None), 'is_update_allowed() must be implemented.'),
        ('is_delete_allowed', (None,), 'is_delete_allowed() must be implemented.'),
    ))
    def test_not_implemented_method_raise_exception(self, method_name: str, args: tuple[None, ...], expected_msg: str) -> None:
        with pytest.raises(NotImplementedError) as exc_info:
            get_method(self.crud_base_not_implemented, method_name)(*args)
        check_exception_info(exc_info, expected_msg)

    @pytest_mark_anyio
    @pytest.mark.parametrize('method_name', ('update', 'delete'))
    async def test_update_delete_raise_not_found_exceptions(self, method_name: str) -> None:
        expected_msg=self.msg_not_found
        await self._update_delete_raise_exceptions(method_name, HTTPException, expected_msg, not_found=True)

    @pytest_mark_anyio
    @pytest.mark.parametrize('method_name, expected_msg', (
        ('update', 'is_update_allowed() must be implemented.'),
        ('delete', 'is_delete_allowed() must be implemented.'),
    ))
    async def test_update_delete_raise_is_allowed_exceptions(self, method_name: str, expected_msg: str) -> None:
        await self._update_delete_raise_exceptions(method_name, NotImplementedError, expected_msg, self._create_object)

    @pytest_mark_anyio
    @pytest.mark.parametrize('method_name', ('update', 'delete'))
    async def test_update_delete_raise_has_permission_exceptions(self, method_name: str) -> None:
        expected_msg = 'has_permission() must be implemented.'
        await self._update_delete_raise_exceptions(method_name, NotImplementedError, expected_msg, self._create_object, user=1)

    async def _update_delete_raise_exceptions(self, method_name, exc_type, expected_msg, func=None, user=None, not_found=False):
        method = get_method(self.crud_base_not_implemented, method_name)
        args = (1,) if method_name == 'delete' else (1, self.update_schema(**self.update_payload))
        if func is not None:
            await func()
        with pytest.raises(exc_type) as exc_info:
            await method(*args, user=user)
        check_exception_info_not_found(exc_info, self.msg_not_found) if not_found else check_exception_info(exc_info, expected_msg)
