from collections.abc import Callable
from typing import Any

from amsdal_glue_connections.sql.sql_builders.operator_constructor import repr_operator_constructor
from amsdal_glue_connections.sql.sql_builders.query_builder import build_where
from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeySchema
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.operations.mutations.schema import AddConstraint
from amsdal_glue_core.common.operations.mutations.schema import AddIndex
from amsdal_glue_core.common.operations.mutations.schema import AddProperty
from amsdal_glue_core.common.operations.mutations.schema import DeleteConstraint
from amsdal_glue_core.common.operations.mutations.schema import DeleteIndex
from amsdal_glue_core.common.operations.mutations.schema import DeleteProperty
from amsdal_glue_core.common.operations.mutations.schema import DeleteSchema
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import RenameProperty
from amsdal_glue_core.common.operations.mutations.schema import RenameSchema
from amsdal_glue_core.common.operations.mutations.schema import SchemaMutation
from amsdal_glue_core.common.operations.mutations.schema import UpdateProperty


def build_schema_mutation(mutation: SchemaMutation, type_transform: Callable[[Any], str]) -> list[str]:
    if isinstance(mutation, RegisterSchema):
        return [
            build_create_table(mutation.schema, type_transform=type_transform),
            *build_create_indexes(mutation.schema.name, mutation.schema.indexes or []),
        ]

    if isinstance(mutation, DeleteSchema):
        return [
            build_drop_table(mutation.schema_reference),
        ]

    if isinstance(mutation, RenameSchema):
        return [
            build_rename_table(mutation.schema_reference, mutation.new_schema_name),
        ]

    if isinstance(mutation, AddProperty):
        return [
            build_add_column(mutation.schema_reference, mutation.property, type_transform=type_transform),
        ]

    if isinstance(mutation, DeleteProperty):
        return [
            build_drop_column(mutation.schema_reference, mutation.property_name),
        ]

    if isinstance(mutation, RenameProperty):
        return [
            build_rename_column(mutation.schema_reference, mutation.old_name, mutation.new_name),
        ]

    if isinstance(mutation, UpdateProperty):
        return [
            build_update_column(mutation.schema_reference, mutation.property, type_transform=type_transform),
        ]

    if isinstance(mutation, AddConstraint):
        return [
            build_full_constraint_stmt(mutation.schema_reference, mutation.constraint),
        ]

    if isinstance(mutation, DeleteConstraint):
        return [
            build_drop_constraint(mutation.schema_reference, mutation.constraint_name),
        ]

    if isinstance(mutation, AddIndex):
        return [
            build_index(mutation.schema_reference.name, mutation.index),
        ]

    if isinstance(mutation, DeleteIndex):
        return [
            build_drop_index(mutation.schema_reference, mutation.index_name),
        ]

    msg = f'Unsupported schema mutation: {type(mutation)}'
    raise ValueError(msg)


def build_create_table(schema: Schema, type_transform: Callable[[Any], str]) -> str:
    if schema.extends is not None:
        msg = f'Unsupported nested schemas: {schema.extends}'
        raise ValueError(msg)

    _constraint_stmts = []

    for _constraint in schema.constraints or []:
        _constraint_stmt = build_constraint(_constraint)
        _constraint_stmts.append(_constraint_stmt)

    stmt = f'CREATE TABLE {schema.name} ('
    stmt += ', '.join(build_column(column, type_transform=type_transform) for column in schema.properties)

    if _constraint_stmts:
        stmt += ', '
        stmt += ', '.join(_constraint_stmts)

    stmt += ')'

    return stmt


def build_create_indexes(schema_name: str, indexes: list[IndexSchema]) -> list[str]:
    return [
        build_index(schema_name, index)
        for index in indexes
    ]


def build_index(schema_name: str, index: IndexSchema) -> str:
    _index = f'CREATE INDEX {index.name} ON {schema_name} ({", ".join(index.fields)})'

    if index.condition:
        where, _ = build_where(index.condition, operator_constructor=repr_operator_constructor)
        _index += f' WHERE {where}'

    return _index


def build_constraint(constraint: BaseConstraint) -> str:
    if isinstance(constraint, PrimaryKeyConstraint):
        return f'CONSTRAINT {constraint.name} ' f'PRIMARY KEY ({", ".join(constraint.fields)}) '
    if isinstance(constraint, ForeignKeySchema):
        return (
            f'CONSTRAINT {constraint.name} '
            f'FOREIGN KEY ({", ".join(constraint.fields)}) '
            f'REFERENCES {constraint.reference_schema.name} ({", ".join(constraint.reference_fields)})'
        )
    if isinstance(constraint, UniqueConstraint):
        return f'CONSTRAINT {constraint.name} ' f'UNIQUE ({", ".join(constraint.fields)})'
    if isinstance(constraint, CheckConstraint):
        _where, _ = build_where(constraint.condition, operator_constructor=repr_operator_constructor)

        return f'CONSTRAINT {constraint.name} ' f'CHECK ({_where})'

    msg = f'Unsupported constraint: {type(constraint)}'
    raise ValueError(msg)


def build_column(column: PropertySchema, type_transform: Callable[[Any], str]) -> str:
    return f'{column.name} {type_transform(column.type)}{" NOT NULL" if column.required else ""}'


def build_drop_table(schema_reference: SchemaReference) -> str:
    return f'DROP TABLE {schema_reference.name}'


def build_rename_table(schema_reference: SchemaReference, new_schema_name: str) -> str:
    return f'ALTER TABLE {schema_reference.name} RENAME TO {new_schema_name}'


def build_add_column(
    schema_reference: SchemaReference,
    property_obj: PropertySchema,
    type_transform: Callable[[Any], str],
) -> str:
    _column = build_column(property_obj, type_transform=type_transform)
    return f'ALTER TABLE {schema_reference.name} ADD COLUMN {_column}'


def build_drop_column(schema_reference: SchemaReference, property_name: str) -> str:
    return f'ALTER TABLE {schema_reference.name} DROP COLUMN {property_name}'


def build_rename_column(schema_reference: SchemaReference, old_name: str, new_name: str) -> str:
    return f'ALTER TABLE {schema_reference.name} RENAME COLUMN {old_name} TO {new_name}'


def build_update_column(
    schema_reference: SchemaReference,
    property_obj: PropertySchema,
    type_transform: Callable[[Any], str],
) -> str:
    _column = build_column(property_obj, type_transform=type_transform)
    return f'ALTER TABLE {schema_reference.name} ALTER COLUMN {_column}'


def build_full_constraint_stmt(schema_reference: SchemaReference, constraint: BaseConstraint) -> str:
    msg = 'SQLite does not support adding constraints to existing tables. Recreate table instead.'
    raise NotImplementedError(msg)


def build_drop_constraint(schema_reference: SchemaReference, constraint_name: str) -> str:  # noqa: ARG002
    msg = 'SQLite does not support dropping constraints from existing tables. Recreate table instead.'
    raise NotImplementedError(msg)


def build_drop_index(schema_reference: SchemaReference, index_name: str) -> str:
    return f'DROP INDEX {index_name} ON {schema_reference.name}'