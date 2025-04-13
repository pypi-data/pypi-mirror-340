from ceonmedia import CstockJobInputType, CstockWebInputType

# Examples that should always work
SUCCESS_CASES = [
    {
        "name": "myTestProjInput",
        "job_input_type": CstockJobInputType.IMG,
        "web_input_type": CstockWebInputType.IMG,
    }
]

# Examples that we know should not work.
FAIL_CASES = [
    {  # Fail unrecognized kwargs to alert user of possible unexpected data inputs if unpacking a dict
        "name": "myTestProjInput",
        "job_input_type": CstockJobInputType.IMG,
        "web_input_type": CstockWebInputType.IMG,
        "unknownKawrgNotRecognized": [1, 2, 3],
    },
    {  # Passed the wrong Enum type to job_input (the passed enum value 'DROPDOWN' doesn't exist on the expected enum)
        "name": "myTestProjInput",
        "job_input_type": CstockWebInputType.DROPDOWN,
        "web_input_type": CstockWebInputType.IMG,
    },
    {  # Passed the wrong Enum type to job_input (but the passed enum value does also exist on the expected enum)
        "name": "myTestProjInput",
        "job_input_type": CstockWebInputType.IMG,
        "web_input_type": CstockWebInputType.IMG,
    },
]
