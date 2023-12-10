import pytest

from tests.conftest import Base, Post

BASE_FIELDS = ('id',)
POST_MODEL_FIELDS = ('id', 'title', 'content', 'created', 'updated', 'likes', 'dislikes', 'author_id', 'author')
POST_SAVE_DATA = {'title': 'Another New post title.', 'content': 'POST New post content.', 'author_id': 1}


class BaseTest(Base):
    pass


@pytest.mark.parametrize('class_, class_fields', (
    (Base, BASE_FIELDS),
    (Post, POST_MODEL_FIELDS),
))
def test_model_fields(class_, class_fields) -> None:
    for field in class_fields:
        assert hasattr(class_, field)


@pytest.mark.parametrize('instance, instance_fields', (
    (BaseTest(), BASE_FIELDS),
    (Post(**POST_SAVE_DATA), POST_MODEL_FIELDS[1:-1]),
))
def test_model_repr(instance, instance_fields) -> None:
    for attr_name in instance_fields:
        assert instance.__repr__().find(attr_name) != -1
