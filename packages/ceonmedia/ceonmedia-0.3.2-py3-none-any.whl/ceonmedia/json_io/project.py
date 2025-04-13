# Import/Export for a ceonmedia Project
# To avoid polluting the base classes implement (de)serialization tools in this module directly,
import json
import logging
from uuid import uuid4
from dataclasses import asdict

from ceonmedia.core import CstockProject, web_input
from ceonmedia.core.project import CstockProjectInfo
from ceonmedia.core.project_input import CstockProjectInput
from ceonmedia import CstockJobInputType
from ceonmedia import CstockWebInputType
from ceonmedia import constants

from ceon_render import (
    CeonFileReference,
    CeonFileSourceType,
    CeonRenderPipeline,
    CeonRenderPipelineJob,
)

logger = logging.getLogger(constants.LOGGER_NAME)

# POSSIBLE ALTERNATIVE dataclass-wizard.
#    https://dataclass-wizard.readthedocs.io/en/latest/
# dataclass_wizard:
# - Expects enums to use VALUES by default: 'color' not 'COLOR'
# - Only provider one error at a time on failure.
# - Doesn't require schema class, just use fromdict and asdict methods directly.
# - Good documentation and seems to be easy to config

# from dataclass_wizard import fromdict, asdict, DumpMeta


# marshmallow:
# - Gives cleaerer errors (reports all together)
# - Expects enums to use NAME not VALUE, e.g. 'COLOR' not 'color'
# - Requires instantiating the schema class first

# Chose to use marshmallow for the multi-error reporting. NOTE: enum NAME vs VALUE could cause
# some compatibility problems with workflows that expect values? It's possible to configures
# marshmallow but haven't looked into it yet and seems to not support enums contained
# within a list?

# Keep dataclass_wizard available as a backup in case the enum naming convention causes problems in the
# future? (Or learn how to configure marshmallow to use enum values)

# import marshmallow_dataclass

# Create a marshmallow schema instance to use for (de)serialization operations.
# project_schema = marshmallow_dataclass.class_schema(CstockProject)()


def _project_input_from_dict(dict_data) -> CstockProjectInput:
    prepared_dict = dict_data
    try:
        # Load from VALUE
        job_input_type = CstockJobInputType(dict_data["job_input_type"])
    except ValueError:
        # Load from NAME
        job_input_type = CstockJobInputType[dict_data["job_input_type"]]
    prepared_dict["job_input_type"] = job_input_type
    prepared_dict["web_input_type"] = CstockWebInputType(dict_data["web_input_type"])
    return CstockProjectInput(**prepared_dict)


def _render_pipeline_job_from_dict(dict_data) -> CeonRenderPipelineJob:
    prepared_dict = dict_data.copy()
    job_input = dict_data["job_input"]

    # Only pass reference type if speicified in dict to prevent overwriting class
    # defaults
    file_reference_args = {"target": job_input["target"]}
    file_reference_type = job_input.get("file_source")
    if file_reference_type:
        file_reference_args["file_source"] = CeonFileSourceType(file_reference_type)
    file_reference = CeonFileReference(**file_reference_args)
    prepared_dict["job_input"] = file_reference

    return CeonRenderPipelineJob(**prepared_dict)


def _render_pipeline_from_dict(dict_data: dict) -> CeonRenderPipeline:
    prepared_dict = dict_data.copy()
    prepared_dict["pipeline_jobs"] = [
        _render_pipeline_job_from_dict(data) for data in dict_data["pipeline_jobs"]
    ]
    return CeonRenderPipeline(**prepared_dict)


def from_dict(dict_data: dict) -> CstockProject:
    """Convert a JSON dict (simple types only) into a CstockProject instance"""
    prepared_dict = dict_data.copy()
    prepared_dict["project_inputs"] = [
        _project_input_from_dict(data) for data in dict_data["project_inputs"]
    ]
    prepared_dict["render_pipeline"] = _render_pipeline_from_dict(
        dict_data["render_pipeline"]
    )
    prepared_dict["project_info"] = CstockProjectInfo(**dict_data["project_info"])
    return CstockProject(**prepared_dict)


def from_file(file_path: str) -> CstockProject:
    with open(file_path, "r") as f:
        data = json.load(f)
    project_id = data.get("project_id")
    if not project_id:
        new_id = uuid4()
        logger.warning(
            "Loaded json file does not contain a project id (%s). Writing to json file new id: %s",
            file_path,
            new_id,
        )
        data["project_id"] = str(uuid4())
        with open(file_path, "w") as f:
            f.write(json.dumps(data, indent=4, sort_keys=True))
        logger.warning("Rewrote json file: %s", file_path)
    project = from_dict(data)
    return project


def to_file(file_path: str, project: CstockProject) -> str:
    """Save a Cstockproject to a json file.
    Returns: The path of the newly saved file as a string"""
    project_dict = asdict(project)
    with open(file_path, "w") as f:
        json.dump(project_dict, f, indent=2)
    return file_path
