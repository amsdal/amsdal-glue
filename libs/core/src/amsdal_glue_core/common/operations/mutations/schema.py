from copy import copy
from dataclasses import dataclass

from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference


@dataclass(kw_only=True)
class SchemaMutation:
    schema_ref: SchemaReference

    def __copy__(self):
        return SchemaMutation(schema_ref=copy(self.schema_ref))


@dataclass(kw_only=True)
class RegisterSchema(SchemaMutation):
    schema: Schema
    if_not_exists: bool = False

    def __copy__(self):
        return RegisterSchema(
            schema_ref=copy(self.schema_ref),
            schema=copy(self.schema),
            if_not_exists=self.if_not_exists,
        )


@dataclass(kw_only=True)
class DeleteSchema(SchemaMutation):
    if_exists: bool = False
    cascade: bool = False

    def __copy__(self):
        return DeleteSchema(schema_ref=copy(self.schema_ref), if_exists=self.if_exists, cascade=self.cascade)


@dataclass(kw_only=True)
class RenameSchema(SchemaMutation):
    new_name: str

    def __copy__(self):
        return RenameSchema(schema_ref=copy(self.schema_ref), new_name=self.new_name)


@dataclass(kw_only=True)
class AddProperty(SchemaMutation):
    property: PropertySchema

    def __copy__(self):
        return AddProperty(schema_ref=copy(self.schema_ref), property=copy(self.property))


@dataclass(kw_only=True)
class DeleteProperty(SchemaMutation):
    property_name: str

    def __copy__(self):
        return DeleteProperty(schema_ref=copy(self.schema_ref), property_name=self.property_name)


@dataclass(kw_only=True)
class RenameProperty(SchemaMutation):
    old_name: str
    new_name: str

    def __copy__(self):
        return RenameProperty(schema_ref=copy(self.schema_ref), old_name=self.old_name, new_name=self.new_name)


@dataclass(kw_only=True)
class UpdateProperty(SchemaMutation):
    property: PropertySchema

    def __copy__(self):
        return UpdateProperty(schema_ref=copy(self.schema_ref), property=copy(self.property))


@dataclass(kw_only=True)
class AddConstraint(SchemaMutation):
    constraint: BaseConstraint
    not_valid: bool = False

    def __copy__(self):
        return AddConstraint(
            schema_ref=copy(self.schema_ref), constraint=copy(self.constraint), not_valid=self.not_valid
        )


@dataclass(kw_only=True)
class DeleteConstraint(SchemaMutation):
    constraint_name: str

    def __copy__(self):
        return DeleteConstraint(schema_ref=copy(self.schema_ref), constraint_name=self.constraint_name)


@dataclass(kw_only=True)
class ValidateConstraint(SchemaMutation):
    constraint_name: str

    def __copy__(self):
        return ValidateConstraint(schema_ref=copy(self.schema_ref), constraint_name=self.constraint_name)


@dataclass(kw_only=True)
class AddIndex(SchemaMutation):
    index: IndexSchema
    if_not_exists: bool = False
    concurrent: bool = False

    def __copy__(self):
        return AddIndex(
            schema_ref=copy(self.schema_ref),
            index=copy(self.index),
            if_not_exists=self.if_not_exists,
            concurrent=self.concurrent,
        )


@dataclass(kw_only=True)
class DeleteIndex(SchemaMutation):
    index_name: str
    if_exists: bool = False
    concurrent: bool = False

    def __copy__(self):
        return DeleteIndex(
            schema_ref=copy(self.schema_ref),
            index_name=self.index_name,
            if_exists=self.if_exists,
            concurrent=self.concurrent,
        )


@dataclass(kw_only=True)
class CreateExtension(SchemaMutation):
    extension_name: str
    if_not_exists: bool = True
    schema_name: str | None = None
    version: str | None = None
    cascade: bool = False

    def __copy__(self):
        return CreateExtension(
            schema_ref=copy(self.schema_ref),
            extension_name=self.extension_name,
            if_not_exists=self.if_not_exists,
            schema_name=self.schema_name,
            version=self.version,
            cascade=self.cascade,
        )


@dataclass(kw_only=True)
class DropExtension(SchemaMutation):
    extension_name: str
    if_exists: bool = True
    cascade: bool = False

    def __copy__(self):
        return DropExtension(
            schema_ref=copy(self.schema_ref),
            extension_name=self.extension_name,
            if_exists=self.if_exists,
            cascade=self.cascade,
        )


@dataclass(kw_only=True)
class TruncateSchema(SchemaMutation):
    restart_identity: bool = False
    cascade: bool = False

    def __copy__(self):
        return TruncateSchema(
            schema_ref=copy(self.schema_ref),
            restart_identity=self.restart_identity,
            cascade=self.cascade,
        )


@dataclass(kw_only=True)
class CreateCollation(SchemaMutation):
    collation_name: str
    provider: str = 'icu'
    locale: str = ''
    deterministic: bool = True

    def __copy__(self):
        return CreateCollation(
            schema_ref=copy(self.schema_ref),
            collation_name=self.collation_name,
            provider=self.provider,
            locale=self.locale,
            deterministic=self.deterministic,
        )


@dataclass(kw_only=True)
class RemoveCollation(SchemaMutation):
    collation_name: str
    if_exists: bool = True

    def __copy__(self):
        return RemoveCollation(
            schema_ref=copy(self.schema_ref),
            collation_name=self.collation_name,
            if_exists=self.if_exists,
        )
