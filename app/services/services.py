from typing import Annotated

# from aioredis import Redis
from fastapi import Depends  # , BackgroundTasks

from app.core import async_session  # get_aioredis, get_async_session
from app.models import Post, User
from app.repositories.db_repository import PostRepository
# from app.repositories.redis_repository import RedisBaseRepository
from app.services.base import BaseService

# from sqlalchemy.ext.asyncio import AsyncSession


# async_session = Annotated[AsyncSession, Depends(get_async_session)]
# redis = Annotated[Redis, Depends(get_aioredis)]


class PostService(BaseService):
    # , redis: redis, bg_tasks: BackgroundTasks):
    def __init__(self, session: async_session):
        # , RedisBaseRepository(redis, 'menu:'), bg_tasks)
        super().__init__(PostRepository(session))

    async def set_cache_on_create(self, post: Post) -> None:
        pass
        # await super().set_cache(post)

    async def set_cache_on_update(self, post: Post) -> None:
        pass
        # await super().set_cache(post)

    async def set_cache_on_delete(self, post: Post) -> None:
        pass
        # await self.redis.delete_obj(post)

    async def get_user_posts(self, user: User, exception: bool = False) -> list[Post] | None:
        pass

    async def like_dislike_post(self, post_id: int, user: User, like: bool = True) -> Post:
        post = await self.db.like_dislike_post(post_id, user, like)
        if self.redis is not None:
            self._add_bg_task_or_execute(self.set_cache, post)


post_service = Annotated[PostService, Depends()]
