import pytest

from tests.conftest import Base, Dish, Menu, Submenu
from tests.fixtures import data as d

COMMON_FIELDS = ('id', 'title', 'description')


@pytest.mark.parametrize('model, attrs', (
    (Dish, (*COMMON_FIELDS, 'price', 'submenu_id', 'submenu')),
    (Submenu, (*COMMON_FIELDS, 'dishes', 'menu_id', 'menu')),
    (Menu, (*COMMON_FIELDS, 'submenus')),
))
def test_model_attr(model: Base, attrs: str) -> None:
    for attr_name in attrs:
        assert hasattr(model, attr_name)


@pytest.mark.parametrize('model, data, attrs', (
    (Dish, d.DISH_POST_PAYLOAD, (*COMMON_FIELDS, 'price')),
    (Menu, d.MENU_POST_PAYLOAD, (*COMMON_FIELDS, 'submenus_count', 'dishes_count')),
    (Submenu, d.SUBMENU_POST_PAYLOAD, (*COMMON_FIELDS, 'dishes_count')),
))
def test_model_repr(model: Base, data: dict[str, str], attrs: str) -> None:
    representation = str(model(**data))
    for attr_name in attrs:
        assert representation.find(attr_name) != -1
