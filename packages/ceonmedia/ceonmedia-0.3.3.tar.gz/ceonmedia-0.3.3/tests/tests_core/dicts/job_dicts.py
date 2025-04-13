from . import job_input_dicts
from uuid import uuid4

SUCCESS_CASES = [
    {  # Without job_uuid
        "job_inputs": [job_input_dicts.SUCCESS_CASES[0]],
        "job_type": "preview",
        # Valid but non-existant uuid
        "project_uuid": str(uuid4()),
        # No job_uuid provided
    },
    {  # With job_uuid
        "job_inputs": [job_input_dicts.SUCCESS_CASES[0]],
        "job_type": "preview",
        # Valid but non-existant uuid
        "project_uuid": str(uuid4()),
        "job_uuid": str(uuid4())
        # No job_uuid provided
    },
]

FAIL_CASES = [
    {"job_type": "preview", "project_uuid": str(uuid4())}  # Missing job inputs
]
