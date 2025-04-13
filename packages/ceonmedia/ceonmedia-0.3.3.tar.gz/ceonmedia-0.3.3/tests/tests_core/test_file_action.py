import logging
from ceonmedia.core.project_input import CstockProjectInput
from ceonmedia.core.file_action import CstockFileAction
from ceonmedia.core.job_input import CstockJobInputType
from ceonmedia.core.web_input import CstockWebInputType

from . import serialization, instantiation
from .dicts import file_action_dicts

logger = logging.getLogger(__name__)

TEST_CLS = CstockFileAction
TEST_DICTS = file_action_dicts


def test_file_action_dict_serialization() -> None:
    for test_dict in TEST_DICTS.SUCCESS_CASES:
        test_object = TEST_CLS(**test_dict)
        serialization.run_dict_serialization_tests(cstock_object=test_object)


def test_file_action_instantiation_success_cases():
    logger.info("Testing predefined success cases ...")
    instantiation.test_instantiation_success_cases(
        cstock_cls=TEST_CLS, dicts_to_test=TEST_DICTS.SUCCESS_CASES
    )


def test_file_action_instantiation_fail_cases():
    logger.info("Testing predefined fail cases...")
    instantiation.test_instantiation_fail_cases(
        cstock_cls=TEST_CLS, dicts_to_test=TEST_DICTS.FAIL_CASES
    )
