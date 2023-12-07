from typing import Annotated

from fastapi import BackgroundTasks, Depends

from app.core import async_redis, async_session
from app.models import Post, User
from app.repositories import PostRepository, RedisBaseRepository
from app.services import BaseService

# async_session = Annotated[AsyncSession, Depends(get_async_session)]
# async_redis = Annotated[Redis, Depends(get_aioredis)]


class PostService(BaseService):
    def __init__(self, session: async_session, redis: async_redis, bg_tasks: BackgroundTasks):
        super().__init__(PostRepository(session), RedisBaseRepository(redis, 'post:'), bg_tasks)

    async def set_cache_on_create(self, post: Post) -> None:
        await super().set_cache(post)

    async def set_cache_on_update(self, post: Post) -> None:
        await super().set_cache(post)

    async def set_cache_on_delete(self, post: Post) -> None:
        await self.redis.delete_obj(post)

    async def get_user_posts(self, user: User, exception: bool = False) -> list[Post] | None:
        return await self.db.get_user_posts(user, exception)

    async def like_dislike_post(self, post_id: int, user: User, like: bool = True) -> Post:
        post = await self.db.like_dislike_post(post_id, user, like)
        if self.redis is not None:
            await self._add_bg_task_or_execute(self.set_cache, post)
        return post


post_service = Annotated[PostService, Depends()]
