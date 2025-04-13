import logging
import sys
from pathlib import Path

ceon_render_dev_dir = (
    "/mnt/FileStorage/Dayne/Web/proj_ceonmedia/assets/python/ceon_render"
)
sys.path.append(ceon_render_dev_dir)


from ceonmedia import json_io

# from ceonmedia import CstockProjInput, CstockRenderTask
# from ceonmedia import CstockProject
# from ceonmedia.core.project import CstockProjectInfo
from ceonmedia.log import formatters, printify

# from ceonmedia.filesystem import CstockLocalProject
from ceonmedia import json_io

# Logger setup
root_logger = logging.getLogger()
sh = logging.StreamHandler()
sh.setFormatter(formatters.DEV)
root_logger.addHandler(sh)
root_logger.setLevel("DEBUG")

logger = logging.getLogger(__name__)

PROJECTS_DIR = (
    "/mnt/FileStorage/Dayne/Web/proj_ceonmedia/assets/my_cstock_projects"
)
PROJECT_FLDR = "Waving_Flag"
PROJECT_PATH = Path(PROJECTS_DIR, PROJECT_FLDR)


def test_io_project():
    """Load a project and then export it."""
    file_to_load = "/mnt/FileStorage/Dayne/Web/proj_ceonmedia/assets/python/ceonmedia/tests/test_json_io/ceonmedia_project.json"
    if not Path(file_to_load).exists():
        raise FileNotFoundError(f"File not found: {file_to_load}")
    loaded_project = json_io.project.from_file(file_to_load)
    print(loaded_project)

    print("Saving...")
    out_file = Path(file_to_load).with_name("testprojectoutput.json")
    json_io.project.to_file(str(out_file), loaded_project)
    print(f"Saved: {out_file}")


def test_io_job():
    """Load a job and then export it."""
    file_to_load = "/mnt/FileStorage/Dayne/Web/proj_ceonmedia/assets/python/ceonmedia/tests/test_json_io/ceonmedia_job.json"
    if not Path(file_to_load).exists():
        raise FileNotFoundError(f"File not found: {file_to_load}")
    loaded_project = json_io.job.from_file(file_to_load)
    print(loaded_project)

    print("Saving...")
    out_file = Path(file_to_load).with_name("testjoboutput.json")
    json_io.job.to_file(str(out_file), loaded_project)
    print(f"Saved: {out_file}")


def old_stuff():
    # Proj Inputs
    # proj_input1 = CstockProjInput(
    #     name="my_proj_input_1",
    #     job_input_type=CstockProjInput.job_input_types.IMG,
    #     web_input_type=CstockProjInput.web_input_types.IMG,
    # )

    # local_project = CstockLocalProject(f"{PROJECT_PATH}")
    # print()
    # logger.info("Got local project: ")
    # logger.info(printify(local_project))
    # print()

    # json_data = local_project.json()
    # print()
    # logger.info("Got local project json: ")
    # logger.info(printify(json_data))
    # print()

    # cstock_project = local_project.load()
    # print()
    # logger.info("Got loaded_data: ")
    # logger.info(cstock_project)
    # print()

    # # Test export
    # local_project_export_file = "test_project_export.json"
    # print()
    # as_json = json_io.exporter.dumps(cstock_project)
    # logger.info(f"As json:\n{as_json}")
    # with open("local_project_export_file.json", "w+") as f:
    #     f.write(as_json)
    # logger.warning(f"Writtent to file: {local_project_export_file}")

    # Render Tasks
    # render_task1 = CstockRenderTask(
    #     name="my_render_task",
    #     app_type=CstockRenderTask.app_types.HOU,
    #     app_version="19.5",
    #     target_file="relpath/to/file.hiplc",
    #     output="render_output.$F4.exr",
    #     app_render_settings={},
    # )
    # render_tasks = [render_task1, render_task2]

    # test_io_project()
    pass


def main():
    test_io_job()
    test_io_project()


if __name__ == "__main__":
    main()
