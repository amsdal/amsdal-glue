from typing import Any

from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_glue_core.common.operations.mutations.data import DeleteData
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateData

from amsdal_glue_connections.sql.sql_builders.query_builder import build_conditions
from amsdal_glue_connections.sql.sql_builders.transform import Transform
from amsdal_glue_connections.sql.sql_builders.transform import TransformTypes


def build_sql_data_command(
    mutation: DataMutation,
    transform: Transform,
) -> tuple[str, list[Any]]:
    """
    Builds an SQL command for the given data mutation.

    Args:
        mutation (DataMutation): The data mutation to be converted to an SQL command.
        transform (Transform): The transform SQL to database specific.
    Returns:
        tuple[str, list[Any]]: The SQL command and the list of values.
    """
    if isinstance(mutation, InsertData):
        return _build_sql_insert_data(
            mutation,
            transform=transform,
        )

    if isinstance(mutation, UpdateData):
        return _build_sql_update_data(
            mutation,
            transform=transform,
        )

    if isinstance(mutation, DeleteData):
        return _build_sql_delete_data(
            mutation,
            transform=transform,
        )

    msg = f'Unsupported command type: {type(mutation)}'
    raise NotImplementedError(msg)


def _build_sql_insert_data(
    command: InsertData,
    transform: Transform,
) -> tuple[str, list[Any]]:
    _namespace = transform.apply(TransformTypes.TABLE_QUOTE, command.schema.namespace)
    _table = transform.apply(TransformTypes.TABLE_QUOTE, command.schema.name)
    _stmt = transform.apply(TransformTypes.TABLE_SEPARATOR, _namespace, _table)

    stmt = f'INSERT INTO {_stmt}'

    if not command.data:
        msg = 'No data provided for insert operation'
        raise ValueError(msg)

    values: list[Any] = []

    keys = sorted({key for data in command.data for key in data.data})

    placeholders = [
        [transform.apply(TransformTypes.VALUE_PLACEHOLDER, data.data.get(key), transform=transform) for key in keys]
        for data in command.data
    ]
    stmt += ' ('
    stmt += ', '.join(f'{transform.apply(TransformTypes.FIELD_QUOTE, key)}' for key in keys)
    stmt += ') VALUES '
    stmt += ', '.join(f'({", ".join(row)})' for row in placeholders)
    values.extend(transform.apply(TransformTypes.VALUE, data.data.get(key)) for data in command.data for key in keys)

    return stmt, values


def _build_sql_update_data(
    command: UpdateData,
    transform: Transform,
) -> tuple[str, list[Any]]:
    _namespace = transform.apply(TransformTypes.TABLE_QUOTE, command.schema.namespace)
    _table = transform.apply(TransformTypes.TABLE_QUOTE, command.schema.name)
    _stmt = transform.apply(TransformTypes.TABLE_SEPARATOR, _namespace, _table)

    stmt = f'UPDATE {_stmt}'

    if command.schema.alias:
        _alias = transform.apply(TransformTypes.TABLE_QUOTE, command.schema.alias)
        stmt += f' AS {_alias}'

    if not command.data:
        msg = 'No data provided for update operation'
        raise ValueError(msg)

    values: list[Any] = []
    keys = sorted(set(command.data.data))
    key_placeholders = [
        (
            key,
            transform.apply(TransformTypes.VALUE_PLACEHOLDER, command.data.data.get(key), transform=transform),
        )
        for key in keys
    ]

    stmt += ' SET '
    stmt += ', '.join(
        f'{transform.apply(TransformTypes.FIELD_QUOTE, key)} = {placeholder}' for key, placeholder in key_placeholders
    )
    values.extend(transform.apply(TransformTypes.VALUE, command.data.data.get(key)) for key in keys)

    if command.query:
        where, where_values = build_conditions(
            conditions=command.query,
            transform=transform,
        )

        stmt += f' WHERE {where}'
        values.extend(where_values)

    return stmt, values


def _build_sql_delete_data(
    command: DeleteData,
    transform: Transform,
) -> tuple[str, list[Any]]:
    _namespace = transform.apply(TransformTypes.TABLE_QUOTE, command.schema.namespace)
    _table = transform.apply(TransformTypes.TABLE_QUOTE, command.schema.name)
    _stmt = transform.apply(TransformTypes.TABLE_SEPARATOR, _namespace, _table)

    stmt = f'DELETE FROM {_stmt}'  # noqa: S608

    if command.schema.alias:
        _alias = transform.apply(TransformTypes.TABLE_QUOTE, command.schema.alias)
        stmt += f' AS {_alias}'

    values = []

    if command.query:
        where, where_values = build_conditions(
            conditions=command.query,
            transform=transform,
        )

        stmt += f' WHERE {where}'
        values.extend(where_values)
    return stmt, values
