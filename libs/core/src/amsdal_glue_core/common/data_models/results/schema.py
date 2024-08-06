from dataclasses import dataclass

from amsdal_glue_core.common.data_models.results.base import ResultBase
from amsdal_glue_core.common.data_models.schema import Schema


@dataclass(kw_only=True)
class SchemaResult(ResultBase):
    """Represents the result of a schema query operation.

    Attributes:
        success (bool): Indicates whether the operation was successful.
        message (str | None): Optional message providing additional information about the result.
        exception (Exception | None): Optional exception that was raised during the operation, if any.
        schemas (list[Schema | None] | None): The schemas returned by the query operation, if any.
    """

    schemas: list[Schema | None] | None = None
