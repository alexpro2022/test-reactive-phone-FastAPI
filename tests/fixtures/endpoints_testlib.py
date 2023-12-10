"""
Тесты для проверки эндпойнтов.
Реализованы стандартные проверки статус кодов, сообщений и ответных данных
при валидных и не валидных значениях в именах эндпойнтов, параметров пути и
в ключах словарей параметров запроса, тела запроса и данных формы(data).
Проверку валидных и не валидных значений этих словарей необходимо реализовывать отдельно.
"""

from http import HTTPStatus
from typing import Any

from httpx import AsyncClient, Response

DONE = 'DONE'


def __dummy_func(*args, **kwargs) -> str:
    return DONE


def assert_status(response: Response, expected_status_code: int | tuple[int, ...]) -> None:
    if isinstance(expected_status_code, int):
        expected_status_code = (expected_status_code,)
    assert response.status_code in expected_status_code, (response.status_code, expected_status_code,
                                                          response.headers, response.text)


def assert_msg(response: Response, expected_msg: str | None) -> None:
    if expected_msg is not None:
        assert response.json()['detail'] == expected_msg, (response.json().get('detail'), expected_msg)


def get_invalid(item: int | str | dict) -> tuple:
    invalid_str = (None, '', ' ', '-invalid-')
    if isinstance(item, int):
        return 0, -1, 10**12
    if isinstance(item, str):
        return invalid_str
    if isinstance(item, dict):
        dicts = []
        for key in item:
            for invalid_key in invalid_str:
                dd = item.copy()
                value = dd.pop(key)
                dd[invalid_key] = value
                dicts.append(dd)
        return None, *dicts


def strip_slashes(item: str | None) -> str:
    return '' if item is None else str(item).lstrip(' /').rstrip(' /').lower()


def create_endpoint(endpoint: str | None, path_param: int | str | None = None) -> str:
    return f'/{strip_slashes(endpoint)}/{strip_slashes(path_param)}'.rstrip(' /')


async def get_response(
    client: AsyncClient,
    method: str,
    endpoint: str,
    *,
    path_param: int | str | None = None,
    params: dict[str, str] | None = None,
    json: dict[str, str] | None = None,
    data: dict | None = None,
    headers: dict | None = None,
) -> Response:
    endpoint = create_endpoint(endpoint, path_param)
    match method.upper():
        case 'GET':
            return await client.get(endpoint, params=params, headers=headers)
        case 'DELETE':
            return await client.delete(endpoint, params=params, headers=headers)
        case 'POST':
            return await client.post(endpoint, params=params, headers=headers, data=data, json=json)
        case 'PUT':
            return await client.put(endpoint, params=params, headers=headers, data=data, json=json)
        case 'PATCH':
            return await client.patch(endpoint, params=params, headers=headers, data=data, json=json)


async def assert_response(
    expected_status_code: int | None,
    client: AsyncClient,
    method: str,
    endpoint: str,
    *,
    path_param: int | str | None = None,
    params: dict[str, str] | None = None,
    data: dict | None = None,
    json: dict[str, str] | None = None,
    headers: dict | None = None,
) -> Response:
    response = await get_response(client, method, endpoint, path_param=path_param, params=params, data=data, json=json, headers=headers)
    if expected_status_code is None:
        match method.upper():
            case 'POST':
                expected_status_code = (HTTPStatus.OK, HTTPStatus.CREATED)
            case 'DELETE':
                expected_status_code = (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
            case _:
                expected_status_code = HTTPStatus.OK
    assert_status(response, expected_status_code)
    return response


async def standard_tests(
    client: AsyncClient,
    method: str,
    endpoint: str,
    *,
    check_uniqueness: bool = True,
    path_param: int | str | None = None,
    params: dict[str, str] | None = None,
    check_params: bool = False,
    json: dict[str, str] | None = None,
    check_json: bool = False,
    data: dict[str, str] | None = None,
    check_data: bool = False,
    headers: dict | None = None,
    func_check_valid_response: Any | None = None,
    msg_already_exists: str | None = None,
    msg_not_found: str | None = None,
) -> None:
    method = method.upper()

    # valid_request_test -----------------------------------------------------------------------------------
    response = await assert_response(
        None, client, method, endpoint, path_param=path_param, params=params, json=json, data=data, headers=headers)
    if method == 'POST' and check_uniqueness:
        # Sequential POST with the same data should get Integrity Error which raises BAD_REQUEST
        r = await assert_response(
            HTTPStatus.BAD_REQUEST, client, method, endpoint, path_param=path_param, params=params, json=json, data=data, headers=headers)
        assert_msg(r, msg_already_exists)
    elif method == 'DELETE':
        # Sequential DELETE with the same data should get NOT_FOUND
        r = await assert_response(
            HTTPStatus.NOT_FOUND, client, method, endpoint, path_param=path_param, params=params, json=json, data=data, headers=headers)
        assert_msg(r, msg_not_found)
    if func_check_valid_response is None:
        func_check_valid_response = __dummy_func
    assert func_check_valid_response(response.json()) == DONE

    # invalid_endpoint_test -----------------------------------------------------------------------------------
    for invalid_endpoint in get_invalid(endpoint):
        r = await assert_response(
            HTTPStatus.NOT_FOUND, client, method, invalid_endpoint, path_param=path_param, params=params, json=json, data=data, headers=headers)  # type: ignore [arg-type]

    # invalid_path_param_test -----------------------------------------------------------------------------------
    if path_param is not None:
        for invalid_path_param in get_invalid(path_param):
            r = await assert_response(
                HTTPStatus.NOT_FOUND, client, method, endpoint, path_param=invalid_path_param, params=params, json=json, data=data, headers=headers)  # type: ignore [arg-type]
            assert_msg(r, msg_not_found)

    # invalid_query_params_keys_test -----------------------------------------------------------------------------------
    if params is not None and check_params:
        for invalid_params_keys in get_invalid(params):
            await assert_response(
                HTTPStatus.UNPROCESSABLE_ENTITY, client, method, endpoint, path_param=path_param, params=invalid_params_keys, json=json, data=data, headers=headers)  # type: ignore [arg-type]

    # invalid_payload_keys_test -----------------------------------------------------------------------------------
    if json is not None and check_json:
        for invalid_json_keys in get_invalid(json):
            print(invalid_json_keys)
            await assert_response(
                HTTPStatus.UNPROCESSABLE_ENTITY, client, method, endpoint, path_param=path_param, params=params, json=invalid_json_keys, data=data, headers=headers)  # type: ignore [arg-type]

    # invalid_form_keys_test -----------------------------------------------------------------------------------
    if data is not None and check_data:
        for invalid_data_keys in get_invalid(data):
            await assert_response(
                HTTPStatus.UNPROCESSABLE_ENTITY, client, method, endpoint, path_param=path_param, params=params, json=json, data=invalid_data_keys, headers=headers)  # type: ignore [arg-type]


async def not_allowed_methods_test(
    client: AsyncClient,
    not_allowed_methods: tuple[str],
    endpoint: str,
    path_param: int | str | None = None,
) -> None:
    for method in not_allowed_methods:
        await assert_response(HTTPStatus.METHOD_NOT_ALLOWED, client, method, endpoint, path_param=path_param)


# === ATHORIZATION ===
async def get_registered(async_client: AsyncClient, user: dict) -> None:
    response = await async_client.post('/auth/register', json=user)
    assert_status(response, (HTTPStatus.OK, HTTPStatus.CREATED))
    auth_user = response.json()
    assert isinstance(auth_user['id'], int)
    assert auth_user['email'] == user['email']
    assert auth_user['is_active'] == True
    assert auth_user['is_superuser'] == False
    assert auth_user['is_verified'] == False


async def get_auth_user_token(async_client: AsyncClient, user: dict | None, registration: bool = True) -> str | None:
    if user is None:
        return None
    if registration:
        await get_registered(async_client, user)
    user = user.copy()
    user['username'] = user['email']
    response = await async_client.post('/auth/jwt/login', data=user)
    assert_status(response, HTTPStatus.OK)
    token = response.json()['access_token']
    assert isinstance(token, str)
    return token


def get_headers(token: str | None) -> dict[str:str] | None:
    return {'Authorization': f'Bearer {token}'} if token is not None else None
