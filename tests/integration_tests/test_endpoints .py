from http import HTTPStatus

import pytest
from fastapi import status
from httpx import AsyncClient

from ..fixtures.data import (AUTH_USER, AUTHOR, DISLIKE_ENDPOINT, ENDPOINT, ID,
                             LIKE_ENDPOINT, MY_POSTS_ENDPOINT,
                             NO_PERMISSION_MSG, NO_SELF_LIKE_DISLIKE_MSG,
                             POST_NOT_FOUND_MSG, POST_PAYLOAD, PUT_PAYLOAD)
from ..fixtures.endpoints_testlib import (assert_msg, assert_response,
                                          get_auth_user_token, get_headers,
                                          standard_tests)
from .utils import (check_created_post, check_disliked_post, check_liked_post,
                    check_posts, check_updated_post, create_post, empty_list,
                    invalid_title_length, json_invalid_values)

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
PATCH = 'PATCH'
DELETE = 'DELETE'
DONE = 'DONE'

# === UNAUTHORIZED USER ===
@pytest.mark.parametrize('method, endpoint, post_id', (
    # (GET, ENDPOINT, None),
    (GET, ENDPOINT, ID),
))
@pytest.mark.asyncio
async def test_unauthorized_user_access(async_client: AsyncClient, method, endpoint, post_id) -> None:
    response = await async_client.get(f'/{endpoint}/{post_id}')
    assert response.status_code == status.HTTP_200_OK  # , response.json()
    # assert response.json() == []
    # assert_response(HTTPStatus.OK, method, endpoint, path_param=post_id)


@pytest.mark.parametrize('method, endpoint, post_id', (
    (POST, ENDPOINT, None),
    (PUT, ENDPOINT, ID),
    (DELETE, ENDPOINT, ID),
    (GET, MY_POSTS_ENDPOINT, None),
    (GET, LIKE_ENDPOINT, ID),
    (GET, DISLIKE_ENDPOINT, ID),
))
def test_unauthorized_user_no_access(method, endpoint, post_id):
    assert_response(HTTPStatus.UNAUTHORIZED, method, endpoint, path_param=post_id)


# === AUTHORIZED USER NOT AUTHOR ===
@pytest.mark.parametrize('method, endpoint, post_id', (
    (GET, ENDPOINT, None),
    (GET, ENDPOINT, ID),
    (POST, ENDPOINT, None),
    (GET, MY_POSTS_ENDPOINT, None),
    (GET, LIKE_ENDPOINT, ID),
    (GET, DISLIKE_ENDPOINT, ID),
))
def test_authorized_not_author_access(new_post, method, endpoint, post_id):
    user_headers = get_headers(get_auth_user_token(AUTH_USER))
    assert_response(HTTPStatus.OK, method, endpoint, path_param=post_id, headers=user_headers, json=PUT_PAYLOAD)


@pytest.mark.parametrize('method, endpoint, post_id', (
    (PUT, ENDPOINT, ID),
    (DELETE, ENDPOINT, ID),
))
def test_authorized_not_author_no_access(new_post, method, endpoint, post_id):
    user_headers = get_headers(get_auth_user_token(AUTH_USER))
    r = assert_response(HTTPStatus.BAD_REQUEST, method, endpoint, path_param=post_id, headers=user_headers, json=PUT_PAYLOAD)
    assert_msg(r, NO_PERMISSION_MSG)


# === AUTHORIZED USER AUTHOR ===
@pytest.mark.parametrize('method, endpoint, post_id', (
    (GET, ENDPOINT, None),
    (GET, ENDPOINT, ID),
    (POST, ENDPOINT, None),
    (GET, MY_POSTS_ENDPOINT, None),
    (PUT, ENDPOINT, ID),
    (DELETE, ENDPOINT, ID),
))
def test_author_access(new_post, method, endpoint, post_id):
    author_headers = new_post
    assert_response(HTTPStatus.OK, method, endpoint, path_param=post_id, headers=author_headers, json=PUT_PAYLOAD)


@pytest.mark.parametrize('method, endpoint, post_id', (
    (GET, LIKE_ENDPOINT, ID),
    (GET, DISLIKE_ENDPOINT, ID),
))
def test_author_no_access(new_post, method, endpoint, post_id):
    author_headers = new_post
    r = assert_response(HTTPStatus.BAD_REQUEST, method, endpoint, path_param=post_id, headers=author_headers)
    assert_msg(r, NO_SELF_LIKE_DISLIKE_MSG)


# === AUTHORIZED USER ADMIN ===
@pytest.mark.parametrize('method, endpoint, post_id', (
    (GET, ENDPOINT, None),
    (POST, ENDPOINT, None),
    (GET, ENDPOINT, ID),
    (PUT, ENDPOINT, ID),
    (DELETE, ENDPOINT, ID),
    (GET, MY_POSTS_ENDPOINT, None),
))
def test_admin_access(new_post, superuser_client, method, endpoint, post_id):
    assert_response(HTTPStatus.OK, method, endpoint, path_param=post_id, json=PUT_PAYLOAD)


@pytest.mark.parametrize('method, endpoint, post_id', (
    (GET, LIKE_ENDPOINT, ID),
    (GET, DISLIKE_ENDPOINT, ID),
))
def test_admin_no_access(new_post, superuser_client, method, endpoint, post_id):
    r = assert_response(HTTPStatus.BAD_REQUEST, method, endpoint, path_param=post_id, json=PUT_PAYLOAD)
    assert_msg(r, NO_SELF_LIKE_DISLIKE_MSG)


# === METHODS ===
@pytest.mark.parametrize('not_allowed_methods, endpoint, post_id ', (
    ((PUT, PATCH, DELETE), ENDPOINT, None),
    ((PATCH, POST), ENDPOINT, ID),
    ((DELETE, PATCH, POST, PUT), LIKE_ENDPOINT, ID),
    ((DELETE, PATCH, POST, PUT), DISLIKE_ENDPOINT, ID),
    ((DELETE, PATCH, POST, PUT), MY_POSTS_ENDPOINT, None),
))
def test_not_allowed_methods(not_allowed_methods, endpoint, post_id ):
    for method in not_allowed_methods:
        assert_response(HTTPStatus.METHOD_NOT_ALLOWED, method, endpoint, path_param=post_id)


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
def test_allowed_methods(user, method, endpoint, post_id, payload, func, msg):
    headers = get_headers(get_auth_user_token(user))
    if method is not POST:
        create_post(post_author_headers=headers) if user is AUTHOR else create_post()
    json_optional = True if method is PUT else False
    standard_tests(method, endpoint, path_param=post_id, headers=headers, json=payload, json_optional=json_optional, func_check_valid_response=func, msg_invalid_path_param=msg)


# === INVALID PAYLOAD VALUES ===
@pytest.mark.parametrize('method, payload, test_func', (
    (POST, POST_PAYLOAD, json_invalid_values),
    (POST, POST_PAYLOAD, invalid_title_length),
    (PUT, PUT_PAYLOAD, json_invalid_values),
    (PUT, PUT_PAYLOAD, invalid_title_length),
))
def test_json_invalid_values(method, payload, test_func):
    headers = get_headers(get_auth_user_token(AUTHOR)) if method is POST else create_post()
    test_func(method, payload, headers)
