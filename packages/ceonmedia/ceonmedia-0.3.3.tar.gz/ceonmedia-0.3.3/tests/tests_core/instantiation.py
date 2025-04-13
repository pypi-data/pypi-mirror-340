import logging
import pytest
from typing import Type
from copy import deepcopy

from ceonmedia.core.base import CstockBaseClass
from ceonmedia.log import printify
from ceonmedia import errors

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


def test_instantiation_success_cases(
    cstock_cls: Type[CstockBaseClass], dicts_to_test: list[dict]
):
    logger.info("Testing success cases...")
    for dict_to_test in dicts_to_test:
        cstock_cls(**dict_to_test)


def test_instantiation_fail_cases(
    cstock_cls: Type[CstockBaseClass], dicts_to_test: list[dict]
):
    logger.info("Testing fail cases...")
    for dict_to_test in dicts_to_test:
        logger.debug(
            f"Instantiating with (fail) dict: {printify(dict_to_test)}"
        )
        # Include TypeError to catch invalid kwargs passed to initiailizer
        with pytest.raises((errors.CstockError, TypeError)):
            cstock_cls(**dict_to_test)


def test_values_for_key(
    cstock_cls: Type[CstockBaseClass],
    base_dict: dict,
    key: str,
    values: list,
):
    """For each item in values_to_test, replace the key_to_test in the base_dict"""
    dict_to_test = deepcopy(base_dict)
    for value in values:
        dict_to_test[key] = value
        cstock_cls(**dict_to_test)
