from ceonmedia import CstockJobInputType, CstockWebInputType

# Examples that should always work
SUCCESS_CASES = [
    {
        "name": "myTestJobInput",
        "job_input_type": CstockJobInputType.IMG,
        "values": ["folder/to/somefile.jpg"],
    },
    {  # Empty values list
        "name": "myTestJobInput",
        "job_input_type": CstockJobInputType.IMG,
        "values": [],
    },
    {  # string instead of enum (lowercase)
        "name": "myTestJobInput",
        "job_input_type": "img",
        "values": ["rel_fldr/to/somefile.jpg"],
    },
    {  # string instead of enum (uppercase)
        "name": "myTestJobInput",
        "job_input_type": "IMG",
        "values": ["rel_fldr/to/somefile.jpg"],
    },
]

# Examples that we know should not work.
FAIL_CASES = [
    {  # Fail unrecognized kwargs to alert user of possible unexpected data inputs if unpacking a dict
        "name": "myTestJobInput",
        "job_input_type": CstockJobInputType.IMG,
        "values": [],
        "unknown_kwarg": [1, 2, 3],
    },
    {  # Fail if 'values' is not a list
        "name": "myTestJobInput",
        "job_input_type": CstockJobInputType.IMG,
        "values": "res_fldr_to_somefile.jpg",
    },
    {  # non-string value instead of enum
        "name": "myTestJobInput",
        "job_input_type": 1,
        "values": ["rel_fldr/to/somefile.jpg"],
    },
    {  # string instead of enum (unrecognized string)
        "name": "myTestJobInput",
        "job_input_type": "TypeThatDoesntExist",
        "values": ["rel_fldr/to/somefile.jpg"],
    },
    {  # Passed the wrong Enum type to job_input (the passed enum value 'dropdown' doesn't exist on the expected enum)
        "name": "myTestJobInput",
        "job_input_type": CstockWebInputType.DROPDOWN,
        "values": ["rel_fldr/to/somefile.jpg"],
    },
    {  # Passed the wrong Enum type to job_input (but the passed enum value 'img' DOES also exist on the expected enum!)
        "name": "myTestJobInput",
        "job_input_type": CstockWebInputType.IMG,
        "values": ["rel_fldr/to/somefile.jpg"],
    },
]
