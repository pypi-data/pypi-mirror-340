import logging
from typing import Type, Optional
from pathlib import Path

from ceonmedia.core.base import CstockBaseClass
from ceonmedia.log import printify
from ceonmedia import json_io

from . import helpers

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

THIS_DIR = Path(__file__).parent
FILE_EXPORT_DIR = f"{THIS_DIR}/json_files/serialization_exports"


def json_to_cstock(
    json_string, cstock_cls: Type[CstockBaseClass]
) -> CstockBaseClass:
    """Loads a json string into a cstock object"""
    logger.debug(f"Converting json to {cstock_cls}...")
    dict_data = json_io.loads(json_string)
    logger.debug(f"Loaded dict_data: {dict_data}")
    # Instantiate cstock_object from dict
    cstock_object = cstock_cls(**dict_data)
    logger.debug(f"Created cstock_object: {cstock_object}")
    return cstock_object


def cstock_to_json(
    cstock_object: CstockBaseClass, write_file: Optional[Path] = None
) -> str:
    logger.debug(f"Converting {cstock_object} to json...")
    dict_data = cstock_object.__dict__
    logger.debug(f"Received dict_data:\n{dict_data}")
    json_string = json_io.dumps(dict_data)
    logger.debug(f"Created json string:\n{json_string}")
    if write_file:
        logger.info(f"Saving JSON to file: {write_file}")
        with open(write_file, "w") as f:
            f.write(json_string)
    return json_string


def test_json_to_cstock(json_string: str, cstock_cls: Type[CstockBaseClass]):
    """Load a cstock object from a json string.
    Convert the new cstock object back to a JSON string and check for equality
    """

    # Load a cstock object from a JSON string
    logger.debug("Converting json to cstock ...")
    cstock_object = json_to_cstock(json_string, cstock_cls)
    # Then convert it back to JSON
    logger.debug("Converting new cstock object back to json ...")
    back_to_json = cstock_to_json(cstock_object)

    # Check for equality
    logger.debug(
        f"\noriginal / cstock / back_to_json\
    \n\t{json_string}\
    \n\t{cstock_object}\
    \n\t{back_to_json}"
    )
    assert json_string == back_to_json


def test_cstock_to_json(cstock_object: CstockBaseClass):
    """Convert a Cstock object to a JSON string.
    Load a cstock object from the JSON string and check for equality"""
    # Load a cstock object from a JSON string
    logger.debug("Converting cstock to JSON ...")
    json_string = cstock_to_json(cstock_object)
    # Then convert it back to JSON
    logger.debug(
        f"Converting json string back to {cstock_object.__class__} ..."
    )
    back_to_cstock = json_to_cstock(json_string, cstock_object.__class__)

    # Check for equality
    logger.debug(
        f"\noriginal / json / back_to_cstock\
    \n\t{cstock_object}\
    \n\t{json_string}\
    \n\t{back_to_cstock}"
    )
    assert cstock_object.__dict__ == back_to_cstock.__dict__


def run_json_serialization_tests(cstock_object: CstockBaseClass):
    # Export the json string to a file for inspection
    filename = f"{cstock_object.__class__.__name__}.json"
    filepath = Path(FILE_EXPORT_DIR, filename)
    json_string = cstock_to_json(cstock_object, write_file=filepath)

    # Begin tests
    test_cstock_to_json(cstock_object)
    test_json_to_cstock(json_string, cstock_object.__class__)
