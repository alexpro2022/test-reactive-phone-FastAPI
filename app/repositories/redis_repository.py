import pickle
from typing import Any

# from aioredis import Redis
from redis import asyncio as aioredis

from app.core import settings

from .base_db_repository import ModelType

serializer = pickle


class RedisBaseRepository:

    def __init__(self,
                 redis: aioredis.Redis,
                 redis_key_prefix_with_delimeter: str = ':',
                 redis_expire: int = settings.redis_expire) -> None:
        self.redis = redis
        self.redis_key_prefix = redis_key_prefix_with_delimeter
        self.redis_expire = redis_expire

    def _get_key(self, key: Any) -> str:
        return f'{self.redis_key_prefix}{key}'

    async def get_obj(self, key: Any) -> ModelType | None:
        key = (key if (isinstance(key, str) and key.startswith(self.redis_key_prefix))  # type: ignore
               else self._get_key(key))
        cache = await self.redis.get(key)
        if cache:
            result = serializer.loads(await self.redis.get(key))
            if result:
                return result
        return None

    async def get_all(self) -> list[ModelType] | None:
        result = [await self.get_obj(key.decode('utf-8')) for key in  # type: ignore
                  await self.redis.keys(f'{self.redis_key_prefix}*')]
        if result and None not in result:
            return result  # type: ignore
        return None

    async def set_obj(self, obj: ModelType) -> None:
        if obj is not None:
            await self.redis.set(self._get_key(obj.id),
                                 serializer.dumps(obj),
                                 ex=self.redis_expire)

    async def set_all(self, objs: list[ModelType]) -> None:
        if objs is not None:
            for obj in objs:
                await self.set_obj(obj)  # type: ignore

    async def delete_obj(self, obj: ModelType) -> None:
        if obj is not None:
            await self.redis.delete(self._get_key(obj.id))
