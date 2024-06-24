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
    schema: Schema

    def get_schema_name(self) -> str:
        return self.schema.name


@dataclass(kw_only=True)
class ChangeSchema(SchemaMutation):
    schema_reference: SchemaReference

    def get_schema_name(self) -> str:
        return self.schema_reference.name


@dataclass(kw_only=True)
class DeleteSchema(ChangeSchema):
    def get_schema_name(self) -> str:
        return self.schema_reference.name


@dataclass(kw_only=True)
class RenameSchema(ChangeSchema):
    new_schema_name: str


@dataclass(kw_only=True)
class AddProperty(ChangeSchema):
    property: PropertySchema


@dataclass(kw_only=True)
class DeleteProperty(ChangeSchema):
    property_name: str


@dataclass(kw_only=True)
class RenameProperty(ChangeSchema):
    old_name: str
    new_name: str


@dataclass(kw_only=True)
class UpdateProperty(ChangeSchema):
    property: PropertySchema


@dataclass(kw_only=True)
class AddConstraint(ChangeSchema):
    constraint: BaseConstraint


@dataclass(kw_only=True)
class DeleteConstraint(ChangeSchema):
    constraint_name: str


@dataclass(kw_only=True)
class AddIndex(ChangeSchema):
    index: IndexSchema


@dataclass(kw_only=True)
class DeleteIndex(ChangeSchema):
    index_name: str
