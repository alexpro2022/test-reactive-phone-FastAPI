from http import HTTPStatus

from httpx import AsyncClient

from ..fixtures.data import AUTHOR, ENDPOINT, POST_PAYLOAD, PUT_PAYLOAD
from ..fixtures.endpoints_testlib import (assert_status, get_auth_user_token,
                                          get_headers)

DONE = 'DONE'


async def create_post(async_client: AsyncClient,
                      user: dict = AUTHOR,
                      post_author_headers: dict[str:str] | None = None,
                      payload: dict = POST_PAYLOAD) -> dict[str:str]:
    if post_author_headers is None:
        post_author_headers = get_headers(await get_auth_user_token(async_client, user))
    r = await async_client.post(ENDPOINT, headers=post_author_headers, json=payload)
    assert_status(r, HTTPStatus.CREATED)
    return post_author_headers


def empty_list(response_json: list) -> str:
    assert response_json == []
    return DONE


def check_post(response_json: dict, payload: dict, user: dict = AUTHOR, updated: bool = False, likes: int = 0, dislikes: int = 0) -> str:
    assert isinstance(response_json, dict)
    assert isinstance(response_json['id'], int)
    assert response_json['created'] is not None
    assert response_json['updated'] is not None if updated else response_json.get('updated') is None
    assert response_json['likes'] == likes
    assert response_json['dislikes'] == dislikes
    assert response_json['title'] == payload['title']
    assert response_json['content'] == payload['content']
    author = response_json['author']
    assert isinstance(author, dict)
    assert isinstance(author['id'], int)
    assert author['email'] == user['email']
    assert author['is_active'] == True
    assert author['is_superuser'] == False
    assert author['is_verified'] == False
    return DONE


def check_posts(response_json: list) -> str:
    assert isinstance(response_json, list)
    return check_post(response_json[0], POST_PAYLOAD)


def check_created_post(response_json: dict) -> str:
    return check_post(response_json, POST_PAYLOAD)


def check_updated_post(response_json: dict) -> str:
    return check_post(response_json, PUT_PAYLOAD, updated=True)


def check_liked_post(response_json: dict) -> str:
    return check_post(response_json, POST_PAYLOAD, likes=1)


def check_disliked_post(response_json: dict) -> str:
    return check_post(response_json, POST_PAYLOAD, dislikes=1)
