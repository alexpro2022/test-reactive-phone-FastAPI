from http import HTTPStatus

import pytest

from ..fixtures.data import (AUTH_USER, DISLIKE_ENDPOINT, ENDPOINT, ID,
                             LIKE_ENDPOINT, MY_POSTS_ENDPOINT,
                             NO_PERMISSION_MSG, NO_SELF_LIKE_DISLIKE_MSG,
                             PUT_PAYLOAD)
from ..fixtures.endpoints_testlib import (assert_msg, assert_response,
                                          get_auth_user_token, get_headers)

DELETE, GET, POST, PUT, PATCH, DONE = 'DELETE', 'GET', 'POST', 'PUT', 'PATCH', 'DONE'
STATUS_OK = (HTTPStatus.OK, HTTPStatus.CREATED)

pytest_mark_anyio = pytest.mark.asyncio


# === UNAUTHORIZED USER ===
@pytest_mark_anyio
@pytest.mark.parametrize('method, endpoint, post_id', (
    (GET, ENDPOINT, None),
    (GET, ENDPOINT, ID),
))
async def test_unauthorized_user_has_access(async_client, new_post, method, endpoint, post_id) -> None:
    await assert_response(HTTPStatus.OK, async_client, method, endpoint, path_param=post_id)


@pytest_mark_anyio
@pytest.mark.parametrize('method, endpoint, post_id', (
    (POST, ENDPOINT, None),
    (PUT, ENDPOINT, ID),
    (DELETE, ENDPOINT, ID),
    (GET, MY_POSTS_ENDPOINT, None),
    (GET, LIKE_ENDPOINT, ID),
    (GET, DISLIKE_ENDPOINT, ID),
))
async def test_unauthorized_user_has_no_access(async_client, method, endpoint, post_id):
    await assert_response(HTTPStatus.UNAUTHORIZED, async_client, method, endpoint, path_param=post_id)


# === AUTHORIZED USER NOT AUTHOR ===
@pytest_mark_anyio
@pytest.mark.parametrize('method, endpoint, post_id', (
    (GET, ENDPOINT, None),
    (GET, ENDPOINT, ID),
    (POST, ENDPOINT, None),
    (GET, MY_POSTS_ENDPOINT, None),
    (GET, LIKE_ENDPOINT, ID),
    (GET, DISLIKE_ENDPOINT, ID),
))
async def test_authorized_not_author_access(async_client, new_post, method, endpoint, post_id):
    user_headers = get_headers(await get_auth_user_token(async_client, AUTH_USER))
    await assert_response(STATUS_OK, async_client, method, endpoint, path_param=post_id, headers=user_headers, json=PUT_PAYLOAD)


@pytest_mark_anyio
@pytest.mark.parametrize('method, endpoint, post_id', (
    (PUT, ENDPOINT, ID),
    (DELETE, ENDPOINT, ID),
))
async def test_authorized_not_author_no_access(async_client, new_post, method, endpoint, post_id):
    user_headers = get_headers(await get_auth_user_token(async_client, AUTH_USER))
    r = await assert_response(HTTPStatus.BAD_REQUEST, async_client, method, endpoint, path_param=post_id, headers=user_headers, json=PUT_PAYLOAD)
    assert_msg(r, NO_PERMISSION_MSG)


# === AUTHORIZED USER AUTHOR ===
@pytest_mark_anyio
@pytest.mark.parametrize('method, endpoint, post_id', (
    (GET, ENDPOINT, None),
    (GET, ENDPOINT, ID),
    (POST, ENDPOINT, None),
    (GET, MY_POSTS_ENDPOINT, None),
    (PUT, ENDPOINT, ID),
    (DELETE, ENDPOINT, ID),
))
async def test_author_access(async_client, new_post, method, endpoint, post_id):
    author_headers = new_post
    await assert_response(STATUS_OK, async_client, method, endpoint, path_param=post_id, headers=author_headers, json=PUT_PAYLOAD)


@pytest_mark_anyio
@pytest.mark.parametrize('method, endpoint, post_id', (
    (GET, LIKE_ENDPOINT, ID),
    (GET, DISLIKE_ENDPOINT, ID),
))
async def test_author_no_access(async_client, new_post, method, endpoint, post_id):
    author_headers = new_post
    r = await assert_response(HTTPStatus.BAD_REQUEST, async_client, method, endpoint, path_param=post_id, headers=author_headers)
    assert_msg(r, NO_SELF_LIKE_DISLIKE_MSG)


# === AUTHORIZED USER ADMIN ===
@pytest_mark_anyio
@pytest.mark.parametrize('method, endpoint, post_id', (
    (GET, ENDPOINT, None),
    (POST, ENDPOINT, None),
    (GET, ENDPOINT, ID),
    (PUT, ENDPOINT, ID),
    (DELETE, ENDPOINT, ID),
    (GET, MY_POSTS_ENDPOINT, None),
))
async def test_admin_access(async_client, new_post, admin_user, method, endpoint, post_id):
    await assert_response(STATUS_OK, async_client, method, endpoint, path_param=post_id, json=PUT_PAYLOAD)


@pytest_mark_anyio
@pytest.mark.parametrize('method, endpoint, post_id', (
    (GET, LIKE_ENDPOINT, ID),
    (GET, DISLIKE_ENDPOINT, ID),
))
async def test_admin_no_access(async_client, new_post, admin_user, method, endpoint, post_id):
    r = await assert_response(HTTPStatus.BAD_REQUEST, async_client, method, endpoint, path_param=post_id, json=PUT_PAYLOAD)
    assert_msg(r, NO_SELF_LIKE_DISLIKE_MSG)
