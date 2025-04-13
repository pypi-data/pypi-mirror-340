import logging
from typing import Type
from copy import deepcopy
from dataclasses import asdict

from ceonmedia.core.base import CstockBaseClass

logger = logging.getLogger(__name__)
# logger.setLevel("INFO")


def test_dict_to_cstock_object(dict_data, cstock_cls: Type[CstockBaseClass]):
    """Test that a dict is cstock loadable
    in both directions"""
    print()
    logger.debug("\ndict_data / to_cstock / back_to_dict ")
    print(f"\t{dict_data}")
    new_cstock_object = cstock_cls(**dict_data)
    print(f"\t{new_cstock_object}")
    back_to_dict = deepcopy(asdict(new_cstock_object))
    print(f"\t{back_to_dict}")
    assert dict_data == back_to_dict


def test_cstock_object_to_dict(cstock_object: CstockBaseClass):
    """
    Convert the cstock_object to a dict.
    Confirm that the created dict can successfully reinstantiate the object
    """
    dict_data = deepcopy(asdict(cstock_object))
    logger.debug("")
    logger.debug("original / dict / back_to_cstock ")
    logger.debug(f"\t{cstock_object}")
    logger.debug(f"\t{dict_data}")
    cstock_from_dict = cstock_object.__class__(**dict_data)
    logger.debug(f"\t{cstock_from_dict}")
    assert asdict(cstock_object) == asdict(cstock_from_dict)


def run_dict_serialization_tests(cstock_object) -> None:
    """Tests conversion to/from class instance and dict"""
    # Dict data
    logger.info("Testing dict/cstock workflows...")
    dict_data = deepcopy(asdict(cstock_object))
    test_cstock_object_to_dict(cstock_object)
    test_dict_to_cstock_object(dict_data, cstock_object.__class__)
