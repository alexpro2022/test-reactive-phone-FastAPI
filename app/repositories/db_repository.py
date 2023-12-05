from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Post, User
from app.repositories.base_db_repository import CRUDBaseRepository


class PostRepository(CRUDBaseRepository):
    OBJECT_ALREADY_EXISTS = 'Пост с таким заголовком уже существует.'
    NOT_FOUND = 'Пост(ы) не найден(ы).'
    PERMISSION_DENIED = 'У вас нет права доступа к данному посту.'
    SELF_LIKE_DISLIKE_DENIED = 'Запрещено ставить LIKE/DISLIKE собственным постам.'

    def __init__(self, session: AsyncSession):
        super().__init__(Post, session)

    def has_permission(self, obj: Post, user: User) -> None:
        """Admin or author are only allowed to update/delete the post."""
        if not (user.is_superuser or user.id == obj.author_id):
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                self.PERMISSION_DENIED)

    def is_delete_allowed(self, obj: Post) -> None:
        """Always allowed in the project."""
        pass

    def is_update_allowed(self, obj: Post, payload: dict) -> None:
        """Always allowed in the project."""
        pass

    async def get_user_posts(self, user: User, exception: bool = False) -> list[Post] | None:
        return await self._get_all_by_attrs(exception, author_id=user.id)

    async def like_dislike_post(self, post_id: int, user: User, like: bool = True) -> Post:
        post: Post = await self.get_or_404(post_id)
        if post.author_id == user.id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                self.SELF_LIKE_DISLIKE_DENIED)
        if like:
            post.likes += 1
        else:
            post.dislikes += 1
        return await self._save(post)
