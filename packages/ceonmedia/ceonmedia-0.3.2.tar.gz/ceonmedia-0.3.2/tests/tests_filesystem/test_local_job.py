import logging
from typing import Union
from pathlib import Path

import pytest

from ceonmedia import filesystem
from ceonmedia import errors

logger = logging.getLogger(__name__)

# Folders that store test jobs
THIS_DIR = Path(__file__).parent
JOBS_DIR_SUCCESS = f"{THIS_DIR}/local_jobs/success"
JOBS_DIR_FAIL = f"{THIS_DIR}/local_jobs/fail"

# A single chosen project to test class functions
JOB_PATH = Path(JOBS_DIR_SUCCESS, "Simple Job")


def list_folders_in_dir(directory: Union[str, Path]):
    directory = Path(directory)  # Cast string to Path
    return [entry for entry in directory.iterdir() if entry.is_dir()]


def test_local_job_load():
    local_job = filesystem.CstockLocalJob(JOB_PATH)
    cstock_job = local_job.load()
    logger.info(f"Loaded CstockProject from local_job:\n{cstock_job=}")
    # TODO validate project data?


def test_local_job_load_success():
    source_dir = JOBS_DIR_SUCCESS
    local_job_dirs = list_folders_in_dir(source_dir)
    if not local_job_dirs:
        raise Exception(f"Success cases not tested: No jobs found in {source_dir}")
    for local_job_dir in local_job_dirs:
        logger.info(f"Testing lcal job fail case: {local_job_dir}")
        local_job = filesystem.CstockLocalJob(local_job_dir)
        cstock_job = local_job.load()
        logger.info(f"Loaded CstockProject from local_job:\n{cstock_job=}")


def test_local_job_load_fail_cases():
    source_dir = JOBS_DIR_FAIL
    local_job_dirs = list_folders_in_dir(source_dir)
    if not local_job_dirs:
        raise Exception(f"Failure cases not tested: No jobs found in {source_dir}")
    for local_job_dir in local_job_dirs:
        logger.info(f"Testing lcal job fail case: {local_job_dir}")
        with pytest.raises((errors.CstockInstantiationError, FileNotFoundError, NotADirectoryError)):
            local_job = filesystem.CstockLocalJob(local_job_dir)
            cstock_job = local_job.load()
