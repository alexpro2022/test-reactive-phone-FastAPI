import asyncio

from tests import conftest as c

'''



# --- Fixtures for endpoints testing -----------------------------------------------
def test_async_client(async_client: c.AsyncClient) -> None:
    assert isinstance(async_client, c.AsyncClient)


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
