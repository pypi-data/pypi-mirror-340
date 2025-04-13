import logging

logger = logging.getLogger(__name__)


def log_dict_equality(orig_dict: dict, new_dict):
    logger.info(f"Checking dict equality...")
    for key in orig_dict:
        orig_value = orig_dict[key]
        new_value = new_dict[key]
        is_equal = orig_value == new_value
        logger.debug(f"Equality matched for key '{key}': {is_equal}")
        log_fn = logger.debug if is_equal else logger.warning
        log_fn(
            f"\nKey '{key}' old '==' new: {is_equal}:\
                \nOrig: ({type(orig_value)}){orig_value}\
                \nNew: ({type(new_value)}){new_value}\
            "
        )
