import logging
from ceonmedia.core import CstockRenderTask
from . import serialization, instantiation
from .dicts import render_task_dicts

logger = logging.getLogger(__name__)

TEST_CLS = CstockRenderTask
TEST_DICTS = render_task_dicts


def test_render_task_dict_serialization() -> None:
    for test_dict in TEST_DICTS.SUCCESS_CASES:
        test_object = TEST_CLS(**test_dict)
        serialization.run_dict_serialization_tests(cstock_object=test_object)


def test_render_task_instantiation_success_cases() -> None:
    logger.info("Testing predefined success cases ...")
    instantiation.test_instantiation_success_cases(
        cstock_cls=TEST_CLS, dicts_to_test=TEST_DICTS.SUCCESS_CASES
    )


def test_render_task_instantiation_fail_cases() -> None:
    logger.info("Testing predefined fail cases...")
    instantiation.test_instantiation_fail_cases(
        cstock_cls=TEST_CLS, dicts_to_test=TEST_DICTS.FAIL_CASES
    )
