from dataclasses import dataclass
from typing import Any
from typing import Optional
from typing import Union

from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.enums import Version


@dataclass(kw_only=True)
class Schema:
    """Represents a schema definition.

    Attributes:
        name (str): The name of the schema.
        version (str | Version): The version of the schema.
        namespace (str): The namespace of the schema. Defaults to an empty string.
        extends (Optional[SchemaReference]): The schema that this schema extends. Defaults to None.
        properties (list[PropertySchema]): The list of properties in the schema.
        constraints (list[BaseConstraint] | None): The list of constraints in the schema. Defaults to None.
        indexes (list[IndexSchema] | None): The list of indexes in the schema. Defaults to None.
    """

    name: str
    version: str | Version
    namespace: str = ''
    extends: Optional['SchemaReference'] = None
    properties: list['PropertySchema']
    constraints: list[BaseConstraint] | None = None
    indexes: list[IndexSchema] | None = None


@dataclass(kw_only=True)
class PropertySchema:
    """Represents a property within a schema.

    Attributes:
        name (str): The name of the property.
        type (Union[Schema, SchemaReference, type[Any]]): The type of the property.
        required (bool): Whether the property is required.
        description (str | None): The description of the property. Defaults to None.
        default (Any | None): The default value of the property. Defaults to None.
    """

    name: str
    type: Union[Schema, 'SchemaReference', type[Any]]
    required: bool
    description: str | None = None
    default: Any | None = None


@dataclass(kw_only=True)
class SchemaReference:
    """Represents a reference to another schema.

    Attributes:
        name (str): The name of the referenced schema.
        version (str | Version): The version of the referenced schema.
        alias (str | None): The alias of the referenced schema. Defaults to None.
        namespace (str | None): The namespace of the referenced schema. Defaults to None.
    """

    name: str
    version: str | Version
    alias: str | None = None
    namespace: str | None = None
