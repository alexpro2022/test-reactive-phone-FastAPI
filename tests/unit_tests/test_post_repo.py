from typing import Callable

import pytest
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.repositories import CRUDBaseRepository, PostRepository
from tests.fixtures.data import AUTH_USER, AUTHOR, POST_PAYLOAD, PUT_PAYLOAD
from tests.integration_tests.utils import create_post


class UserRepositoryTest(CRUDBaseRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(User, session)


class TestPostRepository:
    OBJECT_ALREADY_EXISTS = 'Пост с таким заголовком уже существует.'
    NOT_FOUND = 'Пост(ы) не найден(ы).'
    PERMISSION_DENIED = 'У вас нет прав доступа к данному посту.'
    SELF_LIKE_DISLIKE_DENIED = 'Запрещено ставить LIKE/DISLIKE собственным постам.'
    repo: PostRepository | None = None

    @pytest.fixture
    def init(self, get_test_session: AsyncSession) -> None:
        assert self.repo is None
        self.repo = PostRepository(get_test_session)

    def test_init_fixture(self, init):
        assert isinstance(self.repo, PostRepository)

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
    def test_is_allowed(self, init, method_name):
        args = (None, None) if method_name == 'is_update_allowed' else (None,)
        assert self.repo.__getattribute__(method_name)(*args) is None


    @pytest.mark.asyncio
    async def test_get_users_post(self, init, async_client, get_test_session) -> None:
        async def get_user_by_email(email: EmailStr) -> User:
            return await UserRepositoryTest(get_test_session)._get_by_attrs(email=email)
        for user, payload in ((AUTHOR, POST_PAYLOAD), (AUTH_USER, PUT_PAYLOAD)):
            await create_post(async_client, user=user, payload=payload)
        posts = await self.repo.get_all()
        assert len(posts) == 2
        for user in (AUTHOR, AUTH_USER):
            author = await get_user_by_email(user['email'])
            author_posts = await self.repo.get_user_posts(author)
            assert len(author_posts) == 1
            for post in author_posts:
                assert post in posts
                assert post.author_id == author.id


    @pytest.mark.skip(reason='Not ready yet')
    @pytest.mark.asyncio
    async def test_like_dislike_post(self, init, async_client, get_test_session) -> None:
        await create_post(async_client)
        author: User = await UserRepositoryTest(get_test_session)._get_by_attrs(email=AUTHOR['email'])
        posts = await self.repo.get_user_posts(author)
        for post in posts:
            assert post.author_id == author.id
