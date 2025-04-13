from uuid import UUID, uuid4
from ceonmedia.core.render import CstockRenderPipeline, CstockRenderAppType
from . import json_tests
from ceonmedia.tests.dicts import render_pipeline_dicts


TEST_CLS = CstockRenderPipeline
TEST_DICTS = render_pipeline_dicts


def test_render_pipeline_json_serialization() -> None:
    for test_dict in TEST_DICTS.SUCCESS_CASES:
        test_object = TEST_CLS(**test_dict)
        json_tests.run_json_serialization_tests(cstock_object=test_object)


# TODO setup proper testing/assertion of failure cases
# def test_render_pipeline_json_serialization_fail() -> None:
#     for test_dict in TEST_DICTS.FAIL_CASES:
#         test_object = TEST_CLS(**test_dict)
#         json_tests.run_json_serialization_tests(cstock_object=test_object)
