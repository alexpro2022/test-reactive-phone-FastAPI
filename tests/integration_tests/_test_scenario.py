from httpx import AsyncClient

from tests import conftest as c
from tests.fixtures import data as d


def _check_objs(objs: list[c.Base], model: c.Base, size: int = 1) -> None:
    assert isinstance(objs, list)
    assert len(objs) == size
    for obj in objs:
        assert isinstance(obj, model)


@c.pytest_mark_anyio
async def test_scenario(dish: c.Response,
                        async_client: c.AsyncClient,
                        get_menu_repo: c.MenuRepository,
                        get_submenu_repo: c.SubmenuRepository,
                        get_dish_repo: c.DishRepository):

    # fixture dish - cоздает через API (меню + подменю + блюдо)
    # проверяем наличие
    for repo, model in ((get_menu_repo, c.Menu),
                        (get_submenu_repo, c.Submenu),
                        (get_dish_repo, c.Dish)):
        _check_objs(await repo.get_all(), model)

    # Создает блюдо 2
    response = await async_client.post(d.ENDPOINT_DISH, json=d.DISH_PATCH_PAYLOAD)
    assert response.status_code == 201
    _check_objs(await get_dish_repo.get_all(), c.Dish, 2)

    # Просматривает определенное меню
    response = await async_client.get(f'{d.ENDPOINT_MENU}/1')
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 1
    assert response.json()['dishes_count'] == 2

    # Просматривает определенное подменю
    response = await async_client.get(f'{d.ENDPOINT_SUBMENU}/1')
    assert response.status_code == 200
    assert response.json()['dishes_count'] == 2

    # Удаляет подменю
    response = await async_client.delete(f'{d.ENDPOINT_SUBMENU}/1')
    assert response.status_code == 200

    # Просматривает список подменю
    response = await async_client.get(d.ENDPOINT_SUBMENU)
    assert response.status_code == 200
    assert response.json() == []

    # Просматривает список блюд
    response = await async_client.get(d.ENDPOINT_DISH)
    assert response.status_code == 200
    assert response.json() == []

    # Просматривает определенное меню
    response = await async_client.get(f'{d.ENDPOINT_MENU}/1')
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 0
    assert response.json()['dishes_count'] == 0

    # Удаляет меню
    response = await async_client.delete(f'{d.ENDPOINT_MENU}/1')
    assert response.status_code == 200

    # Просматривает список меню
    response = await async_client.get(d.ENDPOINT_MENU)
    assert response.status_code == 200
    assert response.json() == []
