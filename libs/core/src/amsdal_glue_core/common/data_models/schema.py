from copy import copy
from dataclasses import dataclass
from typing import Any
from typing import Optional
from typing import TypeAlias
from typing import Union

from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.enums import Version

FIELD_TYPE: TypeAlias = Union['NestedSchemaModel', 'ArraySchemaModel', 'DictSchemaModel', type[Any]]


@dataclass(kw_only=True)
class NestedSchemaModel:
    """Represents a complex defined data structure with named properties.

    Attributes:
        properties (dict[str, FIELD_TYPE]): The properties of the nested schema model.
    """

    properties: dict[str, FIELD_TYPE]


@dataclass(kw_only=True)
class ArraySchemaModel:
    """Represents an array of a defined data structure.

    Attributes:
        item_type (FIELD_TYPE): The type of items in the array schema model.
    """

    item_type: FIELD_TYPE


@dataclass(kw_only=True)
class DictSchemaModel:
    """Represents a dictionary of a defined data structure.

    Attributes:
        key_type (type): The type of keys in the dictionary schema model.
        value_type (FIELD_TYPE): The type of values in the dictionary schema model.
    """

    key_type: type
    value_type: FIELD_TYPE


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
    metadata: dict[str, Any] | None = None

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return (
            f'Schema<{self.namespace}.{self.name}_v_{self.version}'
            f':{self.extends}'
            f':{self.properties}'
            f':{self.constraints}'
            f':{self.indexes}>'
        )

    def __copy__(self):
        return Schema(
            name=self.name,
            version=self.version,
            namespace=self.namespace,
            extends=copy(self.extends) if self.extends is not None else None,
            properties=[copy(prop) for prop in self.properties],
            constraints=[copy(constraint) for constraint in self.constraints] if self.constraints is not None else None,
            indexes=[copy(index) for index in self.indexes] if self.indexes is not None else None,
            metadata=self.metadata.copy() if self.metadata is not None else None,
        )


@dataclass(kw_only=True)
class PropertySchema:
    """Represents a property within a schema.

    Attributes:
        name (str): The name of the property.
        type (Union[Schema, SchemaReference, FIELD_TYPE]): The type of the property.
        required (bool): Whether the property is required.
        description (str | None): The description of the property. Defaults to None.
        default (Any | None): The default value of the property. Defaults to None.
    """

    name: str
    type: Union[Schema, 'SchemaReference', FIELD_TYPE]
    required: bool
    description: str | None = None
    default: Any | None = None

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not isinstance(other, PropertySchema):
            return False

        return self.name == other.name and self.type == other.type and self.required == other.required

    def __repr__(self):
        return f'PropertySchema<{self.name}:{self.type}:{self.required}:{self.description}:{self.default}>'

    def __copy__(self):
        return PropertySchema(
            name=self.name,
            type=copy(self.type),
            required=self.required,
            description=self.description,
            default=self.default,
        )


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
    version: str | Version = Version.LATEST
    alias: str | None = None
    namespace: str | None = None
    metadata: dict[str, Any] | None = None

    def __copy__(self):
        return SchemaReference(
            name=self.name,
            version=self.version,
            alias=self.alias,
            namespace=self.namespace,
            metadata=self.metadata,
        )

    def __repr__(self):
        return f'SchemaReference<{self.namespace}.{self.name}__v__{self.version}:{self.alias}>'
