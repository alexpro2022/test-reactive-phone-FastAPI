from http import HTTPStatus

from ..fixtures.data import (AUTHOR, ENDPOINT, INVALID_FIELD_MSG_1,
                             INVALID_FIELD_MSG_2, POST_PAYLOAD, PUT_PAYLOAD)
from ..fixtures.endpoints_testlib import (assert_response, get_auth_user_token,
                                          get_headers)

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
PATCH = 'PATCH'
DELETE = 'DELETE'
DONE = 'DONE'

def _info(obj):
    assert obj == '', (f'\ntype = {type(obj)}\nvalue = {obj}')


def empty_list(response_json: list) -> str:
    assert response_json == []
    return DONE


def create_post(user: dict = AUTHOR, post_author_headers: dict[str:str] | None = None) -> dict[str:str]:
    if post_author_headers is None:
        post_author_headers = get_headers(get_auth_user_token(user))
    # client.post(ENDPOINT, headers=post_author_headers, json=POST_PAYLOAD)
    return post_author_headers


def check_post(response_json: dict, payload: dict, user: dict = AUTHOR, updated: bool = False, likes: int = 0, dislikes: int = 0) -> str:
    assert isinstance(response_json['id'], int)
    assert response_json['created'] is not None
    if updated:
        assert response_json['updated'] is not None
    else:
        assert response_json.get('updated') is None
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
    return check_post(response_json[0], POST_PAYLOAD)


def check_created_post(response_json: dict) -> str:
    return check_post(response_json, POST_PAYLOAD)


def check_updated_post(response_json: dict) -> str:
    return check_post(response_json, PUT_PAYLOAD, updated=True)


def check_liked_post(response_json: dict) -> str:
    return check_post(response_json, POST_PAYLOAD, likes=1)


def check_disliked_post(response_json: dict) -> str:
    return check_post(response_json, POST_PAYLOAD, dislikes=1)


def invalid_title_length(method: str, payload: dict, headers: dict):
    for length, status in ((49, HTTPStatus.OK), (50, HTTPStatus.UNPROCESSABLE_ENTITY)):
        invalid_payload = payload.copy()
        invalid_payload['title'] = 'ab' * length + 'c'
        path_param = 1 if method == PUT else None
        assert_response(status, method, ENDPOINT, path_param=path_param, json=invalid_payload, headers=headers)


def json_invalid_values(method: str, payload: dict, headers: dict):
    empty, space, sequence = '', ' ', 'aaaaaaaaaaaa'
    path_param = 1 if method == PUT else None
    for key in payload:
        invalid_payload = payload.copy()
        for invalid_value in ([], (), {}, empty, space, sequence):
            invalid_payload[key] = invalid_value
            response = assert_response(HTTPStatus.UNPROCESSABLE_ENTITY, method, ENDPOINT, path_param=path_param, json=invalid_payload, headers=headers)
            if invalid_value in (empty, space):
                assert response.json()['detail'][0]['msg'] == INVALID_FIELD_MSG_1
            if invalid_value == sequence:
                assert response.json()['detail'][0]['msg'] == INVALID_FIELD_MSG_2
