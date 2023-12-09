from typing import Any

from deepdiff import DeepDiff
from fastapi import status

from tests.fixtures import data as d
from tests.fixtures.endpoints_testlib import DONE


def get_method(instance: Any, method_name: str):
    method = instance.__getattribute__(method_name)
    assert isinstance(method, type(instance.__init__))
    return method


def compare(left, right) -> None:
    def clean(item) -> dict:
        wanted = '_sa_instance_state'
        d = vars(item).copy()
        if hasattr(d, wanted):
            d.pop(wanted)
        return d

    assert clean(left) == clean(right)
    # diff = DeepDiff(clean(left), clean(right), ignore_order=True)
    # assert not diff, diff


def compare_lists(left: list, right: list) -> None:
    assert left and isinstance(left, list)
    assert right and isinstance(right, list)
    assert len(left) == len(right)
    for l, r in zip(left, right):
        compare(l, r)


def check_exception_info(exc_info, expected_msg: str, expected_error_code: int | None = None) -> None:
    assert expected_msg in exc_info.value.args
    if expected_error_code is not None:
        assert expected_error_code in exc_info.value.args


def check_exception_info_not_found(exc_info, msg_not_found: str) -> None:
    check_exception_info(exc_info, msg_not_found, status.HTTP_404_NOT_FOUND)
