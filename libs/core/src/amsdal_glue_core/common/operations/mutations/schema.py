from abc import ABC
from abc import abstractmethod
from copy import copy
from dataclasses import dataclass

from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference


class SchemaMutation(ABC):
    """
    Abstract base class for schema mutations.

    Methods:
        get_schema_name() -> str:
            Returns the name of the schema associated with the mutation.
    """

    @abstractmethod
    def get_schema_name(self) -> str:
        """
        Returns the name of the schema associated with the mutation.

        Returns:
            str: The name of the schema.
        """
        ...

    @abstractmethod
    def get_schema_reference(self) -> SchemaReference:
        """
        Returns the reference to the schema associated with the mutation.

        Returns:
            SchemaReference: The reference to the schema.
        """
        ...


@dataclass(kw_only=True)
class RegisterSchema(SchemaMutation):
    """Represents a schema registration mutation.

    Attributes:
        schema (Schema): The schema to be registered.
    """

    schema: Schema

    def get_schema_name(self) -> str:
        return self.schema.name

    def get_schema_reference(self) -> SchemaReference:
        return SchemaReference(name=self.schema.name, version=self.schema.version)

    def __copy__(self):
        return RegisterSchema(schema=copy(self.schema))


@dataclass(kw_only=True)
class ChangeSchema(SchemaMutation):
    """Represents a schema change mutation.

    Attributes:
        schema_reference (SchemaReference): The reference to the schema to be changed.
    """

    schema_reference: SchemaReference

    def get_schema_name(self) -> str:
        return self.schema_reference.name

    def get_schema_reference(self) -> SchemaReference:
        return copy(self.schema_reference)

    def __copy__(self):
        return ChangeSchema(schema_reference=copy(self.schema_reference))


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

    def __copy__(self):
        return RenameSchema(schema_reference=copy(self.schema_reference), new_schema_name=self.new_schema_name)


@dataclass(kw_only=True)
class AddProperty(ChangeSchema):
    """Represents an add property mutation.

    Attributes:
        property (PropertySchema): The property to be added.
    """

    property: PropertySchema

    def __copy__(self):
        return AddProperty(schema_reference=copy(self.schema_reference), property=copy(self.property))


@dataclass(kw_only=True)
class DeleteProperty(ChangeSchema):
    """Represents a delete property mutation.

    Attributes:
        property_name (str): The name of the property to be deleted.
    """

    property_name: str

    def __copy__(self):
        return DeleteProperty(schema_reference=copy(self.schema_reference), property_name=self.property_name)


@dataclass(kw_only=True)
class RenameProperty(ChangeSchema):
    """Represents a rename property mutation.

    Attributes:
        old_name (str): The current name of the property.
        new_name (str): The new name for the property.
    """

    old_name: str
    new_name: str

    def __copy__(self):
        return RenameProperty(
            schema_reference=copy(self.schema_reference), old_name=self.old_name, new_name=self.new_name
        )


@dataclass(kw_only=True)
class UpdateProperty(ChangeSchema):
    """Represents an update property mutation.

    Attributes:
        property (PropertySchema): The property to be updated.
    """

    property: PropertySchema

    def __copy__(self):
        return UpdateProperty(schema_reference=copy(self.schema_reference), property=copy(self.property))


@dataclass(kw_only=True)
class AddConstraint(ChangeSchema):
    """Represents an add constraint mutation.

    Attributes:
        constraint (BaseConstraint): The constraint to be added.
    """

    constraint: BaseConstraint

    def __copy__(self):
        return AddConstraint(schema_reference=copy(self.schema_reference), constraint=copy(self.constraint))


@dataclass(kw_only=True)
class DeleteConstraint(ChangeSchema):
    """Represents a delete constraint mutation.

    Attributes:
        constraint_name (str): The name of the constraint to be deleted.
    """

    constraint_name: str

    def __copy__(self):
        return DeleteConstraint(schema_reference=copy(self.schema_reference), constraint_name=self.constraint_name)


@dataclass(kw_only=True)
class AddIndex(ChangeSchema):
    """Represents an add index mutation.

    Attributes:
        index (IndexSchema): The index to be added.
    """

    index: IndexSchema

    def __copy__(self):
        return AddIndex(schema_reference=copy(self.schema_reference), index=copy(self.index))


@dataclass(kw_only=True)
class DeleteIndex(ChangeSchema):
    """Represents a delete index mutation.

    Attributes:
        index_name (str): The name of the index to be deleted.
    """

    index_name: str

    def __copy__(self):
        return DeleteIndex(schema_reference=copy(self.schema_reference), index_name=self.index_name)
