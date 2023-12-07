from typing import Callable

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import PostRepository
from tests.utils import info


class TestPostRepository:
    OBJECT_ALREADY_EXISTS = 'Пост с таким заголовком уже существует.'
    NOT_FOUND = 'Пост(ы) не найден(ы).'
    PERMISSION_DENIED = 'У вас нет прав доступа к данному посту.'
    SELF_LIKE_DISLIKE_DENIED = 'Запрещено ставить LIKE/DISLIKE собственным постам.'
    repo: PostRepository

    @pytest.fixture
    def init(self, get_test_session: AsyncSession) -> None:
        self.repo = PostRepository(get_test_session)

    def test_messages(self) -> None:
        def get_class_vars_consts(class_):
            return [attr for attr in class_.__dict__ if (not isinstance(getattr(class_, attr), Callable) and not attr.startswith('__'))]
        test_attrs = get_class_vars_consts(self.__class__)
        post_attrs = get_class_vars_consts(PostRepository)
        assert test_attrs == post_attrs
        for attr in test_attrs:
            assert getattr(self, attr) == getattr(PostRepository, attr)

    @pytest.mark.parametrize('method_name', ('is_delete_allowed', 'is_update_allowed'))
    def test_is_allowed(self, init, method_name):
        args = (None, None) if method_name == 'is_update_allowed' else (None,)
        assert self.repo.__getattribute__(method_name)(*args) is None
