from uuid import uuid4
from ceonmedia.core import CstockRenderAppType
from ceonmedia.core import render_task

SUCCESS_CASES = [
    {  # Expected case
        "task_name": "myTestRenderTask",
        "app_type": CstockRenderAppType.HOU,
        "app_version": "19.5",
        "app_render_settings": render_task.CstockRenderTaskAppSettingsHou(
            frames="0 10", target_node="/out/karma1"
        ),
        "task_input": "relpath/to/somefile/my_project_hip.hiplc",
        "task_output": "relpath/to/otuputfile/todo/figure_out_proper_approach",
        "task_dependencies": [],
    },
    {  # App from string
        "task_name": "myTestRenderTask",
        "app_type": "hou",
        "app_version": "19.5",
        "app_render_settings": render_task.CstockRenderTaskAppSettingsHou(
            frames="0 10", target_node="/out/karma1"
        ),
        "task_input": "relpath/to/somefile/my_project_hip.hiplc",
        "task_output": "relpath/to/otuputfile/todo/figure_out_proper_approach",
        "task_dependencies": [],
    },
    {  # Render settings from dict
        "task_name": "myTestRenderTask",
        "app_type": CstockRenderAppType.HOU,
        "app_version": "19.5",
        "app_render_settings": {
            "frames": "0 10",
            "target_node": "/out/karma1",
        },
        "task_input": "relpath/to/somefile/my_project_hip.hiplc",
        "task_output": "relpath/to/otuputfile/todo/figure_out_proper_approach",
        "task_dependencies": [],
    },
    {  # With UUID object
        "task_name": "myTestRenderTask",
        "app_type": CstockRenderAppType.HOU,
        "app_version": "19.5",
        "app_render_settings": render_task.CstockRenderTaskAppSettingsHou(
            frames="0 10", target_node="/out/karma1"
        ),
        "task_input": "relpath/to/somefile/my_project_hip.hiplc",
        "task_output": "relpath/to/otuputfile/todo/figure_out_proper_approach",
        "task_uuid": uuid4(),
        "task_dependencies": [],
    },
    {  # With UUID (as string)
        "task_name": "myTestRenderTask",
        "app_type": CstockRenderAppType.HOU,
        "app_version": "19.5",
        "app_render_settings": render_task.CstockRenderTaskAppSettingsHou(
            frames="0 10", target_node="/out/karma1"
        ),
        "task_input": "relpath/to/somefile/my_project_hip.hiplc",
        "task_output": "relpath/to/otuputfile/todo/figure_out_proper_approach",
        "task_uuid": str(uuid4()),
        "task_dependencies": [],
    },
]

FAIL_CASES = [
    {  # Invalid app string
        "task_name": "myTestRenderTask",
        "app_type": "fakeapp_type",
        "app_version": "19.5",
        "task_input": "relpath/to/somefile/my_project_hip.hiplc",
        "task_output": "path/to/otuputfile/todo/figure_out_proper_approach",
        "task_dependencies": [],
    },
    {  # With invalid uuid string (non-hex chars)
        "task_name": "myTestRenderTask",
        "app_type": CstockRenderAppType.HOU,
        "app_version": "19.5",
        "task_input": "relpath/to/somefile/my_project_hip.hiplc",
        "task_output": "relpath/to/otuputfile/todo/figure_out_proper_approach",
        "task_uuid": "invalidwithillegalchars",
        "task_dependencies": [],
    },
    {  # With invalid uuid string (too long) (but using only valid hex chars)
        "task_name": "myTestRenderTask",
        "app_type": CstockRenderAppType.HOU,
        "app_version": "19.5",
        "task_input": "relpath/to/somefile/my_project_hip.hiplc",
        "task_output": "relpath/to/otuputfile/todo/figure_out_proper_approach",
        "task_uuid": "0a47c1dc-47e1-4c22-ac51-0800bd5024c63",
        "task_dependencies": [],
    },
]
