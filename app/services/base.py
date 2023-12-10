"""
This is a base service class implementation.
Please override set_cache_on_xxx methods with extra logic for Redis in the inherited class.
    * xxx - create/update/delete
"""
from typing import Any

import pydantic
from fastapi import BackgroundTasks

from app.repositories import CRUDBaseRepository, ModelType
from app.repositories.redis_repository import RedisBaseRepository


class BaseService:
    """Base abstract service class."""
    MSG_NOT_IMPLEMENTED = "Method or function hasn't been implemented yet."

    def __init__(self,
                 db: CRUDBaseRepository,
                 redis: RedisBaseRepository | None = None,
                 bg_tasks: BackgroundTasks | None = None) -> None:
        self.db = db
        self.redis = redis
        self.bg_tasks = bg_tasks

    async def _add_bg_task_or_execute(self, method, obj: ModelType | list[ModelType]) -> None:
        if obj:
            self.bg_tasks.add_task(method, obj) if self.bg_tasks is not None else await method(obj)

    async def set_cache(self, obj: ModelType | list[ModelType]) -> None:
        if obj:
            await self.redis.set_all(obj) if isinstance(obj, list) else await self.redis.set_obj(obj)

    async def __get(
        self, method_name: str | None = None, pk: int | None = None, exception: bool = False
    ) -> ModelType | None:
        obj = None
        if self.redis is not None:
            obj = await self.redis.get_all() if pk is None else await self.redis.get_obj(pk)
        if not obj:
            obj = await self.db.get_all(exception) if pk is None else await self.db.__getattribute__(method_name)(pk)
            if self.redis is not None:
                await self._add_bg_task_or_execute(self.set_cache, obj)
        return obj

    async def get(self, pk: int) -> ModelType | None:
        return await self.__get('get', pk)

    async def get_or_404(self, pk: int) -> ModelType:
        return await self.__get('get_or_404', pk)

    async def get_all(self, exception: bool = False) -> list[ModelType] | None:
        return await self.__get(exception=exception)

# === Hooks ===
    async def set_cache_on_create(self, obj: ModelType) -> None:
        raise NotImplementedError(self.MSG_NOT_IMPLEMENTED)

    async def set_cache_on_update(self, obj: ModelType) -> None:
        raise NotImplementedError(self.MSG_NOT_IMPLEMENTED)

    async def set_cache_on_delete(self, obj: ModelType) -> None:
        raise NotImplementedError(self.MSG_NOT_IMPLEMENTED)

    async def create(self, payload: pydantic.BaseModel, **kwargs) -> ModelType:
        """Base class provides database `create` method and
           not implemented `set_cache_on_create` template-method in FastAPI BackgroundTasks or directly."""
        obj = await self.db.create(payload, **kwargs)
        if self.redis is not None:
            await self._add_bg_task_or_execute(self.set_cache_on_create, obj)
        return obj

    async def update(self, pk: int, payload: pydantic.BaseModel, user: Any | None = None, **kwargs) -> ModelType:
        """Base class provides database `update` method and
           not implemented `set_cache_on_update` template-method in FastAPI BackgroundTasks or directly."""
        obj = await self.db.update(pk, payload, user, **kwargs)
        if self.redis is not None:
            await self._add_bg_task_or_execute(self.set_cache_on_update, obj)
        return obj

    async def delete(self, pk: int, user: Any | None = None) -> ModelType:
        """Base class provides database `delete` method and
           not implemented `set_cache_on_delete` template-method in FastAPI BackgroundTasks or directly."""
        obj = await self.db.delete(pk, user)
        if self.redis is not None:
            await self._add_bg_task_or_execute(self.set_cache_on_delete, obj)
        return obj
