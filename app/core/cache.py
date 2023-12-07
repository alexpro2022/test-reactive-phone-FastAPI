from typing import Annotated

import aioredis
from fastapi import Depends

from app.core.config import settings


def get_aioredis() -> aioredis.Redis:
    return aioredis.from_url(settings.redis_url)


async_redis = Annotated[aioredis.Redis, Depends(get_aioredis)]
