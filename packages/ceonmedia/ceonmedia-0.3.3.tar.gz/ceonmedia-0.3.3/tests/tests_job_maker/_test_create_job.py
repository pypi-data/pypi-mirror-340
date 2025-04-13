import logging
from pathlib import Path

from ceonmedia import CstockProject
from ceonmedia import CstockJobInputType
from ceonmedia import CstockProjectInput
from ceonmedia import CstockRenderPipeline
from ceonmedia import CstockRenderTask
from ceonmedia import CstockRenderAppType
from ceonmedia.core import CstockFileReference
from ceonmedia.core.render_task import CstockRenderTaskAppSettingsHou
from ceonmedia.job_maker import value_picker
from ceonmedia.job_maker import job_maker

logger = logging.getLogger(__name__)

JOB_INPUT_FILES_DIR = "/mnt/FileStorage/Dayne/Web/proj_ceonmedia/assets/project_input_files/job_test_rendering_files"
JOBS_DIR = Path("./temp_testfiles_created_jobs").resolve()

# Required to instantiate CstockProject but not relevant in this testcase
RENDER_TASK = CstockRenderTask(
    task_name="hou_render", 
    app_type=CstockRenderAppType.HOU, 
    app_version="20.0", 
    app_render_settings=CstockRenderTaskAppSettingsHou(target_node="/out/karm1", frames="0 25"),
    task_input=CstockFileReference("path/to/hipfile.hiplc"),
    task_output="renderoutput.$F4.png"
)
RENDER_PIPELINE = CstockRenderPipeline(render_tasks=[RENDER_TASK], output_task="hou_render")

PROJECT_INPUTS = {
    "img": CstockProjectInput(
        name="single_image",
        job_input_type=CstockJobInputType.IMG,
        web_input_type=CstockProjectInput.web_input_types.IMG,
        description="A single image TODO system to enforce limit on num inputs",
    ),
    "doc": CstockProjectInput(
        name="image_from_doc",
        job_input_type=CstockJobInputType.IMG,
        web_input_type=CstockProjectInput.web_input_types.DOC,
        description="A single image TODO system to enforce limit on num inputs",
    ),
    "col": CstockProjectInput(
        name="single_color",
        job_input_type=CstockJobInputType.COLOR,
        web_input_type=CstockProjectInput.web_input_types.COLOR,
        description="A single color",
    ),
    "dropdown": CstockProjectInput(
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
}

# TODO load projects form a set of dirs / json files?
PROJECTS_TO_TEST = [
    CstockProject(
        project_inputs=[PROJECT_INPUTS["img"], PROJECT_INPUTS["dropdown"]],
        render_pipeline=RENDER_PIPELINE,
    ),
    CstockProject(
        project_inputs=[PROJECT_INPUTS["doc"], PROJECT_INPUTS["col"]],
        render_pipeline=RENDER_PIPELINE,
    ),
]


def test_create_job_random_inputs():
    project = PROJECTS_TO_TEST[0]
    vp = value_picker.JobInputValuePickerFromFilesRandom(JOB_INPUT_FILES_DIR)
    for project in PROJECTS_TO_TEST:
        job = job_maker.create_job_for_project(project, vp, JOBS_DIR)
        logger.info("Created job: ")
        logger.info(f"{job}")
        logger.warning("TODO: Assert job is valid")


def test_create_job_ordered_inputs():
    project = PROJECTS_TO_TEST[0]
    vp = value_picker.JobInputValuePickerFromFilesOrdered(JOB_INPUT_FILES_DIR)
    for project in PROJECTS_TO_TEST:
        job = job_maker.create_job_for_project(project, vp, JOBS_DIR)
        logger.info("Created job: ")
        logger.info(f"{job}")
        logger.warning("TODO: Assert job is valid")
