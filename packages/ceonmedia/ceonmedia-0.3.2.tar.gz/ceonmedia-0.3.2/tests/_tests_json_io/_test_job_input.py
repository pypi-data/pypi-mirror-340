import logging
from ceonmedia import CstockJobInput, CstockJobInputType

from . import json_tests
from ceonmedia.tests.dicts import job_input_dicts

logger = logging.getLogger(__name__)

TEST_CLS = CstockJobInput
TEST_DICTS = job_input_dicts


def test_job_input_json_serialization() -> None:
    for test_dict in TEST_DICTS.SUCCESS_CASES:
        test_object = TEST_CLS(**test_dict)
        json_tests.run_json_serialization_tests(cstock_object=test_object)
