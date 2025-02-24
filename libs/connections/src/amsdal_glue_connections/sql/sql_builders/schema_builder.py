from collections.abc import Callable
from typing import Any

from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
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

from amsdal_glue_connections.sql.sql_builders.query_builder import build_where
from amsdal_glue_connections.sql.sql_builders.transform import Transform


def build_schema_mutation(  # noqa: C901, PLR0911
    mutation: SchemaMutation,
    type_transform: Callable[[Any], str],
    transform: Transform,
) -> list[tuple[str, list[Any]]]:
    """
    Builds SQL statements for the given schema mutation.

    Args:
        mutation (SchemaMutation): The schema mutation to be converted to SQL statements.
        type_transform (Callable[[Any], str]): The function to transform types.

    Returns:
        list[str]: The list of SQL statements.
    """
    if isinstance(mutation, RegisterSchema):
        return [
            build_create_table(mutation.schema, type_transform=type_transform, transform=transform),
            *build_create_indexes(
                mutation.schema.name,
                mutation.schema.namespace,
                mutation.schema.indexes or [],
                transform=transform,
            ),
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
            build_index(
                mutation.schema_reference.name,
                mutation.schema_reference.namespace or '',
                mutation.index,
                transform=transform,
            ),
        ]

    if isinstance(mutation, DeleteIndex):
        return [
            build_drop_index(mutation.schema_reference, mutation.index_name),
        ]

    msg = f'Unsupported schema mutation: {type(mutation)}'
    raise ValueError(msg)


def build_create_table(
    schema: Schema,
    type_transform: Callable[[Any], str],
    transform: Transform,
) -> tuple[str, list[Any]]:
    if schema.extends is not None:
        msg = f'Unsupported nested schemas: {schema.extends}'
        raise ValueError(msg)

    _constraint_stmts = []
    _values = []

    for _constraint in schema.constraints or []:
        _constraint_stmt, _constraint_values = build_constraint(_constraint, transform=transform)
        _constraint_stmts.append(_constraint_stmt)
        _values.extend(_constraint_values)

    _namespace_prefix = f"'{schema.namespace}'." if schema.namespace else ''
    stmt = f"CREATE TABLE {_namespace_prefix}'{schema.name}' ("
    stmt += ', '.join(build_column(column, type_transform=type_transform) for column in schema.properties)

    if _constraint_stmts:
        stmt += ', '
        stmt += ', '.join(_constraint_stmts)

    stmt += ')'

    return stmt, _values


def build_create_indexes(
    schema_name: str,
    namespace: str,
    indexes: list[IndexSchema],
    transform: Transform,
) -> list[tuple[str, list[Any]]]:
    return [build_index(schema_name, namespace, index, transform=transform) for index in indexes]


def build_index(schema_name: str, namespace: str, index: IndexSchema, transform: Transform) -> tuple[str, list[Any]]:
    fields_str = ', '.join(f"'{field}'" for field in index.fields)
    _namespace_prefix = f"'{namespace}'." if namespace else ''
    _index = f"CREATE INDEX {_namespace_prefix}'{index.name}' ON {_namespace_prefix}'{schema_name}' ({fields_str})"
    _values: list[Any] = []

    if index.condition:
        where, _values = build_where(index.condition, transform=transform)
        _index += f' WHERE {where}'

    return _index, _values


def build_constraint(constraint: BaseConstraint, transform: Transform) -> tuple[str, list[Any]]:
    if isinstance(constraint, PrimaryKeyConstraint):
        fields_str = ', '.join(f"'{field}'" for field in constraint.fields)

        return f"CONSTRAINT '{constraint.name}' PRIMARY KEY ({fields_str})", []
    if isinstance(constraint, ForeignKeyConstraint):
        fields_str = ', '.join(f"'{field}'" for field in constraint.fields)

        return (
            f"CONSTRAINT '{constraint.name}' "
            f'FOREIGN KEY ({fields_str}) '
            f'REFERENCES {constraint.reference_schema.name} ({", ".join(constraint.reference_fields)})'
        ), []
    if isinstance(constraint, UniqueConstraint):
        fields_str = ', '.join(f"'{field}'" for field in constraint.fields)

        return f"CONSTRAINT '{constraint.name}' UNIQUE ({fields_str})", []
    if isinstance(constraint, CheckConstraint):
        _where, _values = build_where(constraint.condition, transform=transform, embed_values=True)

        return f"CONSTRAINT '{constraint.name}' CHECK ({_where})", _values

    msg = f'Unsupported constraint: {type(constraint)}'
    raise ValueError(msg)


def build_column(column: PropertySchema, type_transform: Callable[[Any], str]) -> str:
    return f"'{column.name}' {type_transform(column.type)}{' NOT NULL' if column.required else ''}"


def build_drop_table(schema_reference: SchemaReference) -> tuple[str, list[Any]]:
    _namespace_prefix = f"'{schema_reference.namespace}'." if schema_reference.namespace else ''

    return f"DROP TABLE {_namespace_prefix}'{schema_reference.name}'", []


def build_rename_table(schema_reference: SchemaReference, new_schema_name: str) -> tuple[str, list[Any]]:
    _namespace_prefix = f"'{schema_reference.namespace}'." if schema_reference.namespace else ''

    return f"ALTER TABLE {_namespace_prefix}'{schema_reference.name}' RENAME TO '{new_schema_name}'", []


def build_add_column(
    schema_reference: SchemaReference,
    property_obj: PropertySchema,
    type_transform: Callable[[Any], str],
) -> tuple[str, list[Any]]:
    _column = build_column(property_obj, type_transform=type_transform)
    _namespace_prefix = f"'{schema_reference.namespace}'." if schema_reference.namespace else ''

    return f"ALTER TABLE {_namespace_prefix}'{schema_reference.name}' ADD COLUMN {_column}", []


def build_drop_column(schema_reference: SchemaReference, property_name: str) -> tuple[str, list[Any]]:
    _namespace_prefix = f"'{schema_reference.namespace}'." if schema_reference.namespace else ''

    return f"ALTER TABLE {_namespace_prefix}'{schema_reference.name}' DROP COLUMN '{property_name}'", []


def build_rename_column(schema_reference: SchemaReference, old_name: str, new_name: str) -> tuple[str, list[Any]]:
    _namespace_prefix = f"'{schema_reference.namespace}'." if schema_reference.namespace else ''

    return f"ALTER TABLE {_namespace_prefix}'{schema_reference.name}' RENAME COLUMN '{old_name}' TO '{new_name}'", []


def build_migrate_column(schema_reference: SchemaReference, old_field: str, new_field: str) -> tuple[str, list[Any]]:
    _namespace_prefix = f"'{schema_reference.namespace}'." if schema_reference.namespace else ''
    table_name = f"{_namespace_prefix}'{schema_reference.name}'"

    return f"UPDATE {table_name} SET '{new_field}' = {table_name}.'{old_field}'", []  # noqa: S608


def build_update_column(
    schema_reference: SchemaReference,
    property_obj: PropertySchema,
    type_transform: Callable[[Any], str],
) -> tuple[str, list[Any]]:
    _column = build_column(property_obj, type_transform=type_transform)
    _namespace_prefix = f"'{schema_reference.namespace}'." if schema_reference.namespace else ''

    return f"ALTER TABLE {_namespace_prefix}'{schema_reference.name}' ALTER COLUMN {_column}", []


def build_full_constraint_stmt(
    schema_reference: SchemaReference,
    constraint: BaseConstraint,
) -> tuple[str, list[Any]]:
    msg = 'SQLite does not support adding constraints to existing tables. Recreate table instead.'
    raise NotImplementedError(msg)


def build_drop_constraint(
    schema_reference: SchemaReference,
    constraint_name: str,
) -> tuple[str, list[Any]]:
    msg = 'SQLite does not support dropping constraints from existing tables. Recreate table instead.'
    raise NotImplementedError(msg)


def build_drop_index(schema_reference: SchemaReference, index_name: str) -> tuple[str, list[Any]]:
    _namespace_prefix = f"'{schema_reference.namespace}'." if schema_reference.namespace else ''
    return f"DROP INDEX {_namespace_prefix}'{index_name}'", []
