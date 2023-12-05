import pytest
from fastapi import status

from tests import conftest as c
from tests import utils as u
from tests.fixtures import data as d
from tests.fixtures.endpoints_testlib import (not_allowed_methods_test,
                                              standard_tests)

DELETE, GET, POST, PUT, PATCH = 'DELETE', 'GET', 'POST', 'PUT', 'PATCH'
DOUBLE_NONE = (None, None)

pytestmark = c.pytest_mark_anyio


@pytest.mark.parametrize('endpoint', (d.ENDPOINT_DISH, d.ENDPOINT_MENU, d.ENDPOINT_SUBMENU))
async def test_not_allowed_method(async_client: c.AsyncClient, endpoint: str) -> None:
    await not_allowed_methods_test(async_client, (PUT,), endpoint)


@pytest.mark.parametrize('endpoint', (d.ENDPOINT_DISH, d.ENDPOINT_MENU, d.ENDPOINT_SUBMENU, d.ENDPOINT_FULL_LIST))
async def test_get_all_returns_empty_list(async_client: c.AsyncClient, endpoint: str) -> None:
    response = await async_client.get(endpoint)
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == []


@pytest.mark.parametrize('method, endpoint, path_param, payload, msg_already_exists, msg_not_found, check_func', (
    (GET, d.ENDPOINT_MENU, *DOUBLE_NONE, *d.MENU_MSG_PACK, u.check_menu_list),
    (GET, d.ENDPOINT_MENU, d.ID, None, *d.MENU_MSG_PACK, u.check_menu),
    (PATCH, d.ENDPOINT_MENU, d.ID, d.MENU_PATCH_PAYLOAD,
     *d.MENU_MSG_PACK, u.check_menu_updated),
    (DELETE, d.ENDPOINT_MENU, d.ID, None, *d.MENU_MSG_PACK, u.check_menu_deleted),
    # -------------------------------------------------------------------------------------------------
    (GET, d.ENDPOINT_SUBMENU, *DOUBLE_NONE, * \
     d.SUBMENU_MSG_PACK, u.check_submenu_list),
    (GET, d.ENDPOINT_SUBMENU, d.ID, None, *d.SUBMENU_MSG_PACK, u.check_submenu),
    (PATCH, d.ENDPOINT_SUBMENU, d.ID, d.SUBMENU_PATCH_PAYLOAD,
     *d.SUBMENU_MSG_PACK, u.check_submenu_updated),
    (DELETE, d.ENDPOINT_SUBMENU, d.ID, None, * \
     d.SUBMENU_MSG_PACK, u.check_submenu_deleted),
    # -------------------------------------------------------------------------------------------------
    (GET, d.ENDPOINT_DISH, *DOUBLE_NONE, *d.DISH_MSG_PACK, u.check_dish_list),
    (GET, d.ENDPOINT_DISH, d.ID, None, *d.DISH_MSG_PACK, u.check_dish),
    (PATCH, d.ENDPOINT_DISH, d.ID, d.DISH_PATCH_PAYLOAD,
     *d.DISH_MSG_PACK, u.check_dish_updated),
    (DELETE, d.ENDPOINT_DISH, d.ID, None, *d.DISH_MSG_PACK, u.check_dish_deleted),
    # -------------------------------------------------------------------------------------------------
    (GET, d.ENDPOINT_FULL_LIST, *DOUBLE_NONE, *DOUBLE_NONE, u.check_full_list),
))
async def test_standard(dish: c.Response,
                        async_client: c.AsyncClient,
                        get_menu_repo: c.MenuRepository,
                        get_submenu_repo: c.SubmenuRepository,
                        get_dish_repo: c.DishRepository,
                        method: str,
                        endpoint: str,
                        path_param: str,
                        payload: str,
                        msg_already_exists: str,
                        msg_not_found: str,
                        check_func) -> None:
    repo = u.get_crud(endpoint, menu_repo=get_menu_repo,
                      submenu_repo=get_submenu_repo, dish_repo=get_dish_repo)
    assert len(await repo.get_all()) == 1
    await standard_tests(async_client, method, endpoint,
                         path_param=path_param, json=payload,
                         msg_already_exists=msg_already_exists,
                         msg_not_found=msg_not_found,
                         func_check_valid_response=check_func)
    if method == DELETE:
        assert not await repo.get_all()
    else:
        assert len(await repo.get_all()) == 1


async def test_menu_post(async_client: c.AsyncSession, get_menu_repo: c.MenuRepository) -> None:
    assert not await get_menu_repo.get_all()
    await standard_tests(async_client, POST, d.ENDPOINT_MENU,
                         json=d.MENU_POST_PAYLOAD,
                         msg_already_exists=d.MENU_ALREADY_EXISTS_MSG,
                         msg_not_found=d.MENU_NOT_FOUND_MSG,
                         func_check_valid_response=u.check_created_menu)
    assert await get_menu_repo.get_all()


async def test_submenu_post(menu: c.Response, async_client: c.AsyncSession, get_submenu_repo: c.SubmenuRepository) -> None:
    assert await get_submenu_repo.get_all() is None
    await standard_tests(async_client, POST, d.ENDPOINT_SUBMENU,
                         json=d.SUBMENU_POST_PAYLOAD,
                         msg_already_exists=d.SUBMENU_ALREADY_EXISTS_MSG,
                         msg_not_found=d.SUBMENU_NOT_FOUND_MSG,
                         func_check_valid_response=u.check_created_submenu)
    assert await get_submenu_repo.get_all() is not None


async def test_dish_post(submenu: c.Response, async_client: c.AsyncSession, get_dish_repo: c.DishRepository) -> None:
    assert await get_dish_repo.get_all() is None
    await standard_tests(async_client, POST, d.ENDPOINT_DISH,
                         json=d.DISH_POST_PAYLOAD,
                         msg_already_exists=d.DISH_ALREADY_EXISTS_MSG,
                         msg_not_found=d.DISH_NOT_FOUND_MSG,
                         func_check_valid_response=u.check_dish)
    assert await get_dish_repo.get_all() is not None
