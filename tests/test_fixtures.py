import asyncio

from fastapi import Depends

from app.core import current_user
from tests import conftest as c


def test_event_loop_fixture(event_loop) -> None:
    event_loop.run_until_complete(asyncio.sleep(0))


def test_get_test_session(get_test_session: c.AsyncSession) -> None:
    assert isinstance(get_test_session, c.AsyncSession)


@c.pytest_mark_anyio
async def test_get_test_redis(get_test_redis: c.FakeRedis) -> None:
    assert isinstance(get_test_redis, c.FakeRedis)
    assert await get_test_redis.set('key', 'value')
    assert await get_test_redis.get('key') == b'value'
    assert await get_test_redis.set('key', 'value2')
    assert await get_test_redis.get('key') == b'value2'
    assert await get_test_redis.delete('key')
    assert await get_test_redis.get('key') is None


# --- Fixtures for endpoints testing -----------------------------------------------
def test_async_client(async_client: c.AsyncClient) -> None:
    assert isinstance(async_client, c.AsyncClient)


@c.pytest_mark_anyio
async def test_new_post(new_post) -> None:
    assert new_post

'''
@c.pytest_mark_anyio
async def test_superuser_client(superuser_client):
    user = await current_user()
    print(user)
    assert user.id == 1
    assert user.is_active == True
    assert user.is_verified == True
    assert user.is_superuser == True



def test_menu(menu: c.Response) -> None:
    assert menu.status_code == 201, (menu.headers, menu.content)


def test_menu_dynamic(request: c.Request) -> None:
    menu = request.getfixturevalue('menu')
    assert menu.status_code == 201, (menu.headers, menu.content)


def test_submenu(submenu: c.Response) -> None:
    assert submenu.status_code == 201, (submenu.headers, submenu.content)


def test_submenu_dynamic(request: c.Request) -> None:
    submenu = request.getfixturevalue('submenu')
    assert submenu.status_code == 201, (submenu.headers, submenu.content)


def test_dish(dish: c.Response) -> None:
    assert dish.status_code == 201, (dish.headers, dish.content)


def test_dish_dynamic(request: c.Request) -> None:
    dish = request.getfixturevalue('dish')
    assert dish.status_code == 201, (dish.headers, dish.content)


# --- Fixtures for repository testing -----------------------------------------------

'''


'''
def test_get_menu_repo(get_menu_repo: c.MenuRepository) -> None:
    assert isinstance(get_menu_repo, c.MenuRepository)


def test_get_menu_service(get_menu_service: c.MenuService) -> None:
    assert isinstance(get_menu_service, c.MenuService)


def test_get_submenu_repo(get_submenu_repo: c.SubmenuRepository) -> None:
    assert isinstance(get_submenu_repo, c.SubmenuRepository)


def test_get_submenu_service(get_submenu_service: c.SubmenuService) -> None:
    assert isinstance(get_submenu_service, c.SubmenuService)


def test_get_dish_repo(get_dish_repo: c.DishRepository) -> None:
    assert isinstance(get_dish_repo, c.DishRepository)


def test_get_dish_service(get_dish_service: c.DishService) -> None:
    assert isinstance(get_dish_service, c.DishService)
'''
