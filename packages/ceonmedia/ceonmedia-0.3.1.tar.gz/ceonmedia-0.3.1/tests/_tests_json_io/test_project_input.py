import logging
import pytest
from typing import Union
from uuid import UUID, uuid4
from pathlib import Path
from ceonmedia import CstockProjectInput
from ceonmedia import json_io
from ceonmedia import errors

logger = logging.getLogger(__name__)


def _get_json_files_in_dir(dir_to_read: Union[str, Path]) -> list[Path]:
    if not Path(dir_to_read).is_dir():
        raise Exception(
            f"Could not get test files, dir does not exist: {dir_to_read}"
        )
    p = Path(dir_to_read).glob("**/*")
    files = [x for x in p if x.is_file()]
    if not files:
        raise Exception(f"No files found for testing in path: {dir_to_read}")
    return files


TEST_CLS = CstockProjectInput
JSON_FILES_DIR = f"{Path(__file__).parent}/json_files/project_input"
FILE_DIR_SUCCESS = f"{JSON_FILES_DIR}/success"
FILE_DIR_FAILURE = f"{JSON_FILES_DIR}/failure"
FILES_TO_TEST_SUCCESS = _get_json_files_in_dir(FILE_DIR_SUCCESS)
FILES_TO_TEST_FAILURE = _get_json_files_in_dir(FILE_DIR_FAILURE)


def test_render_task_load_from_json_success() -> None:
    logger.info(f"Loading files: {FILES_TO_TEST_SUCCESS}")
    for test_file in FILES_TO_TEST_SUCCESS:
        logger.info(f"Loading file: {test_file}")
        json_data = json_io.load(test_file)
        test_object = TEST_CLS(**json_data)


def test_render_task_load_from_json_failure() -> None:
    logger.info(f"Loading files: {FILES_TO_TEST_FAILURE}")
    for test_file in FILES_TO_TEST_FAILURE:
        with pytest.raises((TypeError, errors.CstockUnknownTypeError)):
            logger.info(f"Loading file: {test_file}")
            json_data = json_io.load(test_file)
            test_object = TEST_CLS(**json_data)
