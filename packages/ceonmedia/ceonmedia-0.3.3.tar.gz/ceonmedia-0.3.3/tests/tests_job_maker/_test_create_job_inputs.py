import logging

from ceonmedia import CstockProjectInput
from ceonmedia import CstockJobInput
from ceonmedia import CstockJobInputType
from ceonmedia.core.web_input import CstockWebInputType

from ceonmedia.job_maker import value_picker
from ceonmedia.job_maker import job_input_maker

logger = logging.getLogger(__name__)


JOB_INPUT_FILES_DIR = "/mnt/FileStorage/Dayne/Web/proj_ceonmedia/assets/project_input_files/job_test_rendering_files"

PROJECT_INPUTS_TO_TEST = [
    CstockProjectInput(
        name="single_image",
        job_input_type=CstockJobInputType.IMG,
        web_input_type=CstockProjectInput.web_input_types.IMG,
        description="A single image TODO system to enforce limit on num inputs",
    ),
    CstockProjectInput(
        name="image_from_doc",
        job_input_type=CstockJobInputType.IMG,
        web_input_type=CstockProjectInput.web_input_types.DOC,
        description="A single image TODO system to enforce limit on num inputs",
    ),
    CstockProjectInput(
        name="single_color",
        job_input_type=CstockJobInputType.COLOR,
        web_input_type=CstockProjectInput.web_input_types.COLOR,
        description="A single color",
    ),
    CstockProjectInput(
        name="dropdown_string",
        job_input_type=CstockJobInputType.STRING,
        web_input_type=CstockProjectInput.web_input_types.DROPDOWN,
        type_settings={
            "dropdown_options": [
                {
                    "value": "dropdown_option_value_0",
                    "label": "Option Label 0",
                },
                {
                    "value": "dropdown_option_value_1",
                    "label": "Option Label 1",
                },
                {
                    "value": "dropdown_option_value_2",
                    "label": "Option Label 2",
                },
            ]
        },
        description="A single image TODO system to enforce limit on num inputs",
    ),
]


def test_create_job_inputs_random_inputs():
    vp = value_picker.JobInputValuePickerFromFilesRandom(JOB_INPUT_FILES_DIR)
    for project_input in PROJECT_INPUTS_TO_TEST:
        new_job_input = job_input_maker.create_job_input(project_input, vp)
        logger.info(f"New job input: {new_job_input}")
    logger.warning("TODO assert expected job_input state")


def test_create_job_inputs_ordered_inputs():
    vp = value_picker.JobInputValuePickerFromFilesOrdered(JOB_INPUT_FILES_DIR)
    for project_input in PROJECT_INPUTS_TO_TEST:
        new_job_input = job_input_maker.create_job_input(project_input, vp)
        _validate_job_input(project_input, new_job_input)
        # TODO global mechanism for validation
        logger.info(f"New job input: {new_job_input}")
    logger.warning("TODO assert expected job_input state")


# TODO global mechanism for validation
def _validate_job_input(
    cstock_project_input: CstockProjectInput, cstock_job_input: CstockJobInput
):
    logger.warning("TODO: Global mechanism for ceonmedia data validation")
    if cstock_project_input.web_input_type == CstockWebInputType.DROPDOWN:
        assert len(cstock_job_input.values) == 1
