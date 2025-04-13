import logging
from ceonmedia.core.project_input import CstockProjectInput
from ceonmedia.core.job_input import CstockJobInputType
from ceonmedia.core.web_input import CstockWebInputType

from . import serialization, instantiation
from .dicts import proj_input_dicts

logger = logging.getLogger(__name__)

TEST_CLS = CstockProjectInput
TEST_DICTS = proj_input_dicts


def test_proj_input_dict_serialization() -> None:
    for test_dict in TEST_DICTS.SUCCESS_CASES:
        test_object = TEST_CLS(**test_dict)
        serialization.run_dict_serialization_tests(cstock_object=test_object)


def test_proj_input_instantiation_success_cases():
    logger.info("Testing predefined success cases ...")
    instantiation.test_instantiation_success_cases(
        cstock_cls=TEST_CLS, dicts_to_test=TEST_DICTS.SUCCESS_CASES
    )

    # Test instantiation with all ENUM types
    logger.info("Testing init with all known CstockJobInputTypes ...")
    instantiation.test_values_for_key(
        cstock_cls=TEST_CLS,
        base_dict=TEST_DICTS.SUCCESS_CASES[0],
        key="job_input_type",
        values=list(CstockJobInputType),
    )
    logger.info("Testing init with all known CstockWebInputType ...")
    instantiation.test_values_for_key(
        cstock_cls=TEST_CLS,
        base_dict=TEST_DICTS.SUCCESS_CASES[0],
        key="web_input_type",
        values=list(CstockWebInputType),
    )


def test_proj_input_instantiation_fail_cases():
    logger.info("Testing predefined fail cases...")
    instantiation.test_instantiation_fail_cases(
        cstock_cls=TEST_CLS, dicts_to_test=TEST_DICTS.FAIL_CASES
    )
