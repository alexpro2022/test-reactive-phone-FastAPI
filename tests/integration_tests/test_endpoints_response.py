from http import HTTPStatus

import pytest

from ..fixtures.data import (AUTH_USER, AUTHOR, DISLIKE_ENDPOINT, ENDPOINT, ID,
                             LIKE_ENDPOINT, MY_POSTS_ENDPOINT,
                             POST_NOT_FOUND_MSG, POST_PAYLOAD, PUT_PAYLOAD)
from ..fixtures.endpoints_testlib import (assert_response, get_auth_user_token,
                                          get_headers, standard_tests)
from .utils import (check_created_post, check_disliked_post, check_liked_post,
                    check_posts, check_updated_post, create_post, empty_list)

DELETE, GET, POST, PUT, PATCH, DONE = 'DELETE', 'GET', 'POST', 'PUT', 'PATCH', 'DONE'

pytest_mark_anyio = pytest.mark.asyncio


@pytest_mark_anyio
@pytest.mark.parametrize('not_allowed_methods, endpoint, post_id ', (
    ((PUT, PATCH, DELETE), ENDPOINT, None),
    ((PATCH, POST), ENDPOINT, ID),
    ((DELETE, PATCH, POST, PUT), LIKE_ENDPOINT, ID),
    ((DELETE, PATCH, POST, PUT), DISLIKE_ENDPOINT, ID),
))
async def test_not_allowed_methods(async_client, admin_user, not_allowed_methods, endpoint, post_id):
    for method in not_allowed_methods:
        await assert_response(HTTPStatus.METHOD_NOT_ALLOWED, async_client, method, endpoint, path_param=post_id)


@pytest_mark_anyio
@pytest.mark.parametrize('user, method, endpoint, post_id, payload, func, msg', (
    (None, GET, ENDPOINT, None, None, check_posts, None),
    (AUTHOR, POST, ENDPOINT, None, POST_PAYLOAD, check_created_post, None),
    (None, GET, ENDPOINT, ID, None, check_created_post, POST_NOT_FOUND_MSG),
    (AUTHOR, PUT, ENDPOINT, ID, PUT_PAYLOAD, check_updated_post, POST_NOT_FOUND_MSG),
    (AUTHOR, DELETE, ENDPOINT, ID, None, check_created_post, POST_NOT_FOUND_MSG),
    (AUTH_USER, GET, LIKE_ENDPOINT, ID, None, check_liked_post, POST_NOT_FOUND_MSG),
    (AUTH_USER, GET, DISLIKE_ENDPOINT, ID, None, check_disliked_post, POST_NOT_FOUND_MSG),
    (AUTHOR, GET, MY_POSTS_ENDPOINT, None, None, check_posts, None),
    (AUTH_USER, GET, MY_POSTS_ENDPOINT, None, None, empty_list, None),
))
async def test_allowed_methods(async_client, user, method, endpoint, post_id, payload, func, msg):
    headers = get_headers(await get_auth_user_token(async_client, user))
    if method is not POST:
        await create_post(async_client, post_author_headers=headers) if user is AUTHOR else await create_post(async_client)
    await standard_tests(async_client, method, endpoint, path_param=post_id, headers=headers, json=payload, func_check_valid_response=func, msg_not_found=msg)
