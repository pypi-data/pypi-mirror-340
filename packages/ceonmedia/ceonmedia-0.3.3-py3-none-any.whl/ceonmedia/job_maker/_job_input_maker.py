import logging

# TODO protocol instead of dependency
from .value_picker import JobInputValuePicker

from ceonmedia.core.project_input import CstockProjectInput
from ceonmedia.core.job_input import CstockJobInput
from ceonmedia.core.job_input import CstockJobInputType


logger = logging.getLogger(__name__)


# def create_job_input(
#     project_input: CstockProjectInput, value_picker: JobInputValuePicker
# ):
#     """
#     Create a job_input instance for the provided project_input
#     """
#     values = value_picker.get_values(project_input, num_values=5)
#     logger.debug(f"{value_picker} Got {len(values)} values:")
#     for value in values:
#         logger.debug(f"\t{value}")

#     return CstockJobInput(
#         name=project_input.name,
#         job_input_type=project_input.job_input_type,
#         values=values,
#     )
