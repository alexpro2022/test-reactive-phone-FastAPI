import pytest

from tests.conftest import Post

POST_MODEL_FIELDS = ('id', 'title', 'content', 'created', 'updated', 'likes', 'dislikes', 'author_id', 'author')
POST_SAVE_DATA = {'title': 'Another New post title.', 'content': 'POST New post content.', 'author_id': 1}


def test_model_fields() -> None:
    for field in POST_MODEL_FIELDS:
        assert hasattr(Post, field)


def test_model_repr() -> None:
    representation = str(Post(**POST_SAVE_DATA))
    for attr_name in POST_MODEL_FIELDS[1:-1]:
        assert representation.find(attr_name) != -1
