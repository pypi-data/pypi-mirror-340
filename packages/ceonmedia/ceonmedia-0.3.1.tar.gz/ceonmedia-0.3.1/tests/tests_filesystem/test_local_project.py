import logging
from typing import Union
from pathlib import Path

import pytest

from ceonmedia import filesystem
from ceonmedia import errors

logger = logging.getLogger(__name__)

# Folders that store test projects
THIS_DIR = Path(__file__).parent
PROJECTS_DIR_SUCCESS = f"{THIS_DIR}/local_projects/success"
PROJECTS_DIR_FAIL = f"{THIS_DIR}/local_projects/fail"

# A single chosen project to test class functions
PROJECT_PATH = Path(PROJECTS_DIR_SUCCESS, "Waving Flag")


def list_folders_in_dir(directory: Union[str, Path]):
    directory = Path(directory)  # Cast string to Path
    return [entry for entry in directory.iterdir() if entry.is_dir()]


def test_local_project_load():
    local_project = filesystem.CstockLocalProject(PROJECT_PATH)
    cstock_project = local_project.load()
    logger.info(f"Loaded CstockProject from local_project:\n{cstock_project=}")
    # TODO validate project data?


def test_local_project_load_success():
    source_dir = PROJECTS_DIR_SUCCESS
    local_project_dirs = list_folders_in_dir(source_dir)
    if not local_project_dirs:
        raise Exception(f"Success cases not tested: No projects found in {source_dir}")
    for local_project_dir in local_project_dirs:
        logger.info(f"Testing local project success case: {local_project_dir}")
        local_project = filesystem.CstockLocalProject(local_project_dir)
        cstock_project = local_project.load()
        logger.info(f"Loaded CstockProject from local_project:\n{cstock_project=}")


def test_local_project_load_fail_cases():
    source_dir = PROJECTS_DIR_FAIL
    local_project_dirs = list_folders_in_dir(source_dir)
    if not local_project_dirs:
        raise Exception(f"Failure cases not tested: No projects found in {source_dir}")
    for local_project_dir in local_project_dirs:
        logger.info(f"Testing local project fail case: {local_project_dir}")
        with pytest.raises((errors.CstockInstantiationError, FileNotFoundError, NotADirectoryError)):
            local_project = filesystem.CstockLocalProject(local_project_dir)
            cstock_project = local_project.load()
