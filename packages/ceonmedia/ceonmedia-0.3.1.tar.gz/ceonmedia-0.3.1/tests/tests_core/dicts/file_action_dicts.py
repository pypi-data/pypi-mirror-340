from ceonmedia.core.file_action import CstockFileActionResize
from ceonmedia.core.file_action import CstockFileActionType

# Examples that should always work
SUCCESS_CASES = [
    # TODO missing OPTIONAL kwarg.
    {
        # As raw strings/dict
        "action_type": "crop",
        "action_kwargs": {"x": 20, "y": 20, "width": 30, "height": 40},
    },
    {
        # As raw strings/dict
        "action_type": "resize",
        "action_kwargs": {"max_width": 1920, "max_height": 1080},
    },
    {
        # with enum instance as type
        "action_type": CstockFileActionType.RESIZE,
        "action_kwargs": {"max_width": 1920, "max_height": 1080},
    },
    {
        # With class instance nested in dict
        "action_type": "resize",
        "action_kwargs": CstockFileActionResize(
            max_width=1920, max_height=1080
        ),
    },
    {
        # With enum and class instance as args.
        "action_type": CstockFileActionType.RESIZE,
        "action_kwargs": CstockFileActionResize(
            max_width=1920, max_height=1080
        ),
    },
    {
        # With class instance nested in dict
        "action_type": "resize",
        "action_kwargs": CstockFileActionResize(
            max_width=1920, max_height=1080
        ),
    },
]

# Examples that we know should not work.
FAIL_CASES = [
    {
        # Invalid parm name
        "action_type": "resize",
        "action_kwargs": {"typo_kwargname": 1920, "max_height": 1080},
    },
    {
        # Args are valid for CROP type, but not for this action_type.
        "action_type": "resize",
        "action_kwargs": {"x": 20, "y": 20, "width": 30, "height": 40},
    },
    {
        # Missing required crop kwarg 'y'
        "action_type": "crop",
        "action_kwargs": {"x": 20, "width": 30, "height": 40},
    },
]
