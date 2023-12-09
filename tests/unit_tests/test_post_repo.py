from typing import Callable

import pytest
import pytest_asyncio
from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Post, User
from app.repositories import CRUDBaseRepository, PostRepository
from tests.fixtures.data import AUTH_USER, AUTHOR, POST_PAYLOAD, PUT_PAYLOAD
from tests.integration_tests.utils import create_post
from tests.utils import check_exception_info


class UserRepositoryTest(CRUDBaseRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_user_by_email(self, email: EmailStr) -> User:
        return await self._get_by_attrs(email=email)


class TestPostRepository:
    OBJECT_ALREADY_EXISTS = 'Пост с таким заголовком уже существует.'
    NOT_FOUND = 'Пост(ы) не найден(ы).'
    PERMISSION_DENIED = 'У вас нет прав доступа к данному посту.'
    SELF_LIKE_DISLIKE_DENIED = 'Запрещено ставить LIKE/DISLIKE собственным постам.'
    repo: PostRepository | None = None

    @pytest.fixture
    def init_repo(self, get_test_session) -> None:
        assert self.repo is None
        self.repo = PostRepository(get_test_session)

    def test_init_repo_fixture(self, init_repo) -> None:
        assert isinstance(self.repo, PostRepository)

    @pytest_asyncio.fixture
    async def posts(self, init_repo, async_client) -> list[Post]:
        for user, payload in ((AUTHOR, POST_PAYLOAD), (AUTH_USER, PUT_PAYLOAD)):
            await create_post(async_client, user=user, payload=payload)
        return await self.repo.get_all()

    def test_create_posts_fixture(self, posts) -> None:
        assert posts
        assert len(posts) == 2

    def test_messages(self) -> None:
        def get_class_vars_consts(class_):
            return [attr for attr in class_.__dict__ if (
                getattr(class_, attr) is not None
                and not isinstance(getattr(class_, attr), Callable)
                and not attr.startswith('__')
            )]
        test_attrs = get_class_vars_consts(self.__class__)
        post_attrs = get_class_vars_consts(PostRepository)
        assert test_attrs == post_attrs
        for attr in test_attrs:
            assert getattr(self, attr) == getattr(PostRepository, attr)

    @pytest.mark.parametrize('method_name', ('is_delete_allowed', 'is_update_allowed'))
    def test_is_allowed(self, init_repo, method_name):
        args = (None, None) if method_name == 'is_update_allowed' else (None,)
        assert self.repo.__getattribute__(method_name)(*args) is None

    @pytest.mark.asyncio
    async def test_get_users_post(self, get_test_session, posts) -> None:
        for user in (AUTHOR, AUTH_USER):
            author = await UserRepositoryTest(get_test_session).get_user_by_email(user['email'])
            author_posts = await self.repo.get_user_posts(author)
            assert len(author_posts) == 1
            for post in author_posts:
                assert post in posts
                assert post.author_id == author.id

    @pytest.mark.asyncio
    async def test_like_dislike_post_raises_exception(self, get_test_session, posts) -> None:
        author: User = await UserRepositoryTest(get_test_session).get_user_by_email(AUTHOR['email'])
        author_posts = await self.repo.get_user_posts(author)
        for post in author_posts:
            with pytest.raises(HTTPException) as exc_info:
                await self.repo.like_dislike_post(post.id, author)
            check_exception_info(exc_info, self.SELF_LIKE_DISLIKE_DENIED, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('like', (True, False))
    async def test_like_dislike_post(self, get_test_session, posts, like) -> None:
        def check_likes_dislikes(one: int, zero: int):
            assert one == 1
            assert zero == 0

        auth_user: User = await UserRepositoryTest(get_test_session).get_user_by_email(AUTH_USER['email'])
        author: User = await UserRepositoryTest(get_test_session).get_user_by_email(AUTHOR['email'])
        author_posts = await self.repo.get_user_posts(author)
        for post in author_posts:
            obj: Post = await self.repo.like_dislike_post(post.id, auth_user, like)
            args = (obj.likes, obj.dislikes) if like else (obj.dislikes, obj.likes)
            check_likes_dislikes(*args)
