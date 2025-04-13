import logging
from ceonmedia import CstockJob, CstockJobType

from . import serialization, instantiation
from .dicts import job_dicts

logger = logging.getLogger(__name__)

TEST_CLS = CstockJob
TEST_DICTS = job_dicts


def test_job_dict_serialization() -> None:
    for test_dict in TEST_DICTS.SUCCESS_CASES:
        test_object = TEST_CLS(**test_dict)
        serialization.run_dict_serialization_tests(cstock_object=test_object)


def test_job_instantiation_success_cases():
    logger.info("Testing predefined success cases ...")
    instantiation.test_instantiation_success_cases(
        cstock_cls=TEST_CLS, dicts_to_test=TEST_DICTS.SUCCESS_CASES
    )

    logger.info("Testing init with all known CstockJobTypes ...")
    instantiation.test_values_for_key(
        cstock_cls=TEST_CLS,
        base_dict=TEST_DICTS.SUCCESS_CASES[0],
        key="job_type",
        values=list(CstockJobType),
    )

    logger.warning("TODO validate that values are appropriate for job_type")


def test_job_instantiation_fail_cases():
    logger.info("Testing predefined fail cases...")
    instantiation.test_instantiation_fail_cases(
        cstock_cls=TEST_CLS, dicts_to_test=TEST_DICTS.FAIL_CASES
    )
