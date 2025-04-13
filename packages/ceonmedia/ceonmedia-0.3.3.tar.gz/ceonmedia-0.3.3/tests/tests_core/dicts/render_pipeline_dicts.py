from uuid import uuid4
from ceonmedia.core import CstockRenderTask
from ceonmedia.core import render_task
from ceonmedia.core.file_reference import CstockFileReference
from ceonmedia.core.file_reference import CstockFileSourceType
from ceonmedia import CstockRenderPipeline

RENDER_TASKS = [
    CstockRenderTask(
        task_name="render_the_frames",
        task_output="output_file.$r.exr",
        task_input=CstockFileReference("hou_project/myhipfile.hip"),
        app_type=render_task.CstockRenderAppType.HOU,
        app_render_settings=render_task.CstockRenderTaskAppSettingsHou(
            frames="0 10", target_node="/out/karma1"
        ),
        app_version="20.0",
    ),
    CstockRenderTask(
        task_name="ffmpeg_frames_to_mov",
        task_output="my_output.mp4",
        task_input=CstockFileReference(
            "in_file.txt", file_source=CstockFileSourceType.JOB_INPUT
        ),
        app_version="5",
        app_type=render_task.CstockRenderAppType.FFMPEG,
        app_render_settings=render_task.CstockRenderTaskAppSettingsFFMPEG(
            input_args="",
            output_args="",
        ),
    ),
]

SUCCESS_CASES = [
    {  # Expected case
        "render_tasks": RENDER_TASKS,
        "output_task": "ffmpeg_frames_to_mov",
    },
]

FAIL_CASES = [
    {  # No render tasks
        "render_tasks": [],
        "output_task": "ffmpeg_frames_to_mov",
    },
    {  # Primary output task name is not an existing task
        "render_tasks": RENDER_TASKS,
        "output_task": "a_task_name_that_deosnt_exit",
    },
]
