from dataclasses import dataclass
from typing import Any
from typing import Optional
from typing import Union

from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.enums import Version


@dataclass(kw_only=True)
class Schema:
    name: str
    version: str | Version
    extends: Optional['SchemaReference'] = None
    properties: list['PropertySchema']
    constraints: list[BaseConstraint] | None = None
    indexes: list[IndexSchema] | None = None


@dataclass(kw_only=True)
class PropertySchema:
    name: str
    type: Union[Schema, 'SchemaReference', type[Any]]
    required: bool
    description: str | None = None
    default: Any | None = None


@dataclass(kw_only=True)
class SchemaReference:
    name: str
    version: str | Version
    alias: str | None = None
