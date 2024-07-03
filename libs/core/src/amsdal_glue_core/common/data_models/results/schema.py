from dataclasses import dataclass

from amsdal_glue_core.common.data_models.results.base import ResultBase
from amsdal_glue_core.common.data_models.schema import Schema


@dataclass(kw_only=True)
class SchemaResult(ResultBase):
    schemas: list[Schema | None] | None = None
