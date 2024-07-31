from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass

from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference


class SchemaMutation(ABC):
    @abstractmethod
    def get_schema_name(self) -> str: ...


@dataclass(kw_only=True)
class RegisterSchema(SchemaMutation):
    """Represents a schema registration mutation.

    Attributes:
        schema (Schema): The schema to be registered.
    """

    schema: Schema

    def get_schema_name(self) -> str:
        return self.schema.name


@dataclass(kw_only=True)
class ChangeSchema(SchemaMutation):
    """Represents a schema change mutation.

    Attributes:
        schema_reference (SchemaReference): The reference to the schema to be changed.
    """

    schema_reference: SchemaReference

    def get_schema_name(self) -> str:
        return self.schema_reference.name


@dataclass(kw_only=True)
class DeleteSchema(ChangeSchema):
    """Represents a schema deletion mutation."""

    def get_schema_name(self) -> str:
        return self.schema_reference.name


@dataclass(kw_only=True)
class RenameSchema(ChangeSchema):
    """Represents a schema rename mutation.

    Attributes:
        new_schema_name (str): The new name for the schema.
    """

    new_schema_name: str


@dataclass(kw_only=True)
class AddProperty(ChangeSchema):
    """Represents an add property mutation.

    Attributes:
        property (PropertySchema): The property to be added.
    """

    property: PropertySchema


@dataclass(kw_only=True)
class DeleteProperty(ChangeSchema):
    """Represents a delete property mutation.

    Attributes:
        property_name (str): The name of the property to be deleted.
    """

    property_name: str


@dataclass(kw_only=True)
class RenameProperty(ChangeSchema):
    """Represents a rename property mutation.

    Attributes:
        old_name (str): The current name of the property.
        new_name (str): The new name for the property.
    """

    old_name: str
    new_name: str


@dataclass(kw_only=True)
class UpdateProperty(ChangeSchema):
    """Represents an update property mutation.

    Attributes:
        property (PropertySchema): The property to be updated.
    """

    property: PropertySchema


@dataclass(kw_only=True)
class AddConstraint(ChangeSchema):
    """Represents an add constraint mutation.

    Attributes:
        constraint (BaseConstraint): The constraint to be added.
    """

    constraint: BaseConstraint


@dataclass(kw_only=True)
class DeleteConstraint(ChangeSchema):
    """Represents a delete constraint mutation.

    Attributes:
        constraint_name (str): The name of the constraint to be deleted.
    """

    constraint_name: str


@dataclass(kw_only=True)
class AddIndex(ChangeSchema):
    """Represents an add index mutation.

    Attributes:
        index (IndexSchema): The index to be added.
    """

    index: IndexSchema


@dataclass(kw_only=True)
class DeleteIndex(ChangeSchema):
    """Represents a delete index mutation.

    Attributes:
        index_name (str): The name of the index to be deleted.
    """

    index_name: str
