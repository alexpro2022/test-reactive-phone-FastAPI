from typing import Annotated

from fastapi import Depends
# import aioredis
from redis import asyncio as aioredis

from app.core.config import settings


def get_aioredis() -> aioredis.Redis:
    return aioredis.from_url(settings.redis_url)


async_redis = Annotated[aioredis.Redis, Depends(get_aioredis)]
