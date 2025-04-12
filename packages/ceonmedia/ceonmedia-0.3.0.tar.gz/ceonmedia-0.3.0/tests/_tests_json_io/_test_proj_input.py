from ceonstock.core.project_input import CstockProjInput

# from ceonstock.core.job_input import CstockJobInputType
# from ceonstock.core.web_input import CstockWebInputType

from . import json_tests
from ceonstock.tests.dicts import proj_input_dicts

TEST_CLS = CstockProjInput
TEST_DICTS = proj_input_dicts


def test_proj_input_json_serialization() -> None:
    for test_dict in TEST_DICTS.SUCCESS_CASES:
        test_object = TEST_CLS(**test_dict)
        json_tests.run_json_serialization_tests(cstock_object=test_object)
