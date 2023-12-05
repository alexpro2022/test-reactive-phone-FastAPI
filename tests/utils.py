import typing

from deepdiff import DeepDiff
from fastapi import status

from tests.fixtures import data as d
from tests.fixtures.endpoints_testlib import DONE


def _check_response(response_json: dict | list, expected_result: dict | list[dict]) -> str:
    assert response_json == expected_result
    return DONE


def check_created_menu(response_json: dict) -> str:
    return _check_response(response_json, d.CREATED_MENU)


def check_menu(response_json: list) -> str:
    return _check_response(response_json, d.EXPECTED_MENU)


def check_menu_list(response_json: list) -> str:
    return _check_response(response_json, [d.EXPECTED_MENU])


def check_menu_updated(response_json: dict) -> str:
    return _check_response(response_json, d.UPDATED_MENU)


def check_menu_deleted(response_json: dict) -> str:
    return _check_response(response_json, d.DELETED_MENU)


def check_created_submenu(response_json: dict) -> str:
    return _check_response(response_json, d.CREATED_SUBMENU)


def check_submenu(response_json: list) -> str:
    return _check_response(response_json, d.EXPECTED_SUBMENU)


def check_submenu_list(response_json: list) -> str:
    return _check_response(response_json, [d.EXPECTED_SUBMENU])


def check_submenu_updated(response_json: dict) -> str:
    return _check_response(response_json, d.UPDATED_SUBMENU)


def check_submenu_deleted(response_json: dict) -> str:
    return _check_response(response_json, d.DELETED_SUBMENU)


def check_dish(response_json: dict) -> str:
    return _check_response(response_json, d.CREATED_DISH)


def check_dish_list(response_json: list) -> str:
    return _check_response(response_json, [d.CREATED_DISH])


def check_dish_updated(response_json: dict) -> str:
    return _check_response(response_json, d.UPDATED_DISH)


def check_dish_deleted(response_json: dict) -> str:
    return _check_response(response_json, d.DELETED_DISH)


def check_full_list(response_json: dict) -> str:
    return _check_response(response_json, d.EXPECTED_FULL_LIST)


def get_method(instance: typing.Any, method_name: str):
    method = instance.__getattribute__(method_name)
    assert isinstance(method, type(instance.__init__))
    return method


def compare(left, right) -> None:
    for item in (left, right):
        item.__dict__.pop('_sa_instance_state')
    assert left.__dict__ == right.__dict__
    '''
    def _get_attrs(item) -> tuple[str]:
        assert item
        item_attrs = vars(item)  # .__dict__
        try:
            item_attrs.pop('_sa_instance_state')
        except KeyError:
            pass
        return item_attrs
    diff = DeepDiff(_get_attrs(left), _get_attrs(right), ignore_order=True)
    assert not diff, diff
    '''


def compare_lists(left: list, right: list) -> None:
    assert left and right
    assert len(left) == len(right)
    for l, r in zip(left, right):
        compare(l, r)


def check_exception_info(exc_info, expected_msg: str, expected_error_code: int | None = None) -> None:
    assert expected_msg in exc_info.value.args
    if expected_error_code is not None:
        assert expected_error_code in exc_info.value.args


def check_exception_info_not_found(exc_info, msg_not_found: str) -> None:
    check_exception_info(exc_info, msg_not_found, status.HTTP_404_NOT_FOUND)
