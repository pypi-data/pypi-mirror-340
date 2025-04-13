import logging
from typing import Union
from pathlib import Path

import pytest

from ceonmedia import filesystem

logger = logging.getLogger(__name__)

# Folders that store test jobs
THIS_DIR = Path(__file__).parent


class FilenameTest:
    def __init__(self, in_filename: str, expected_output: str):
        self.in_filename = in_filename
        self.expected_output = expected_output


filename_tests_hou_to_ffmpeg = [
    FilenameTest("myrender.$F4.exr", "myrender.%04d.exr"),
]

filename_tests_ffmpeg_to_hou = [
    FilenameTest("myrender.%04.exr", "myrender.$F4.exr"),
]


def test_hou_to_ffmpeg():
    for testcase in filename_tests_hou_to_ffmpeg:
        result = filesystem.filenames.hou_to_ffmpeg(testcase.in_filename)
        assert result == testcase.expected_output


def test_ffmpeg_to_hou():
    for testcase in filename_tests_ffmpeg_to_hou:
        result = filesystem.filenames.ffmpeg_to_hou(testcase.in_filename)
        assert result == testcase.expected_output
