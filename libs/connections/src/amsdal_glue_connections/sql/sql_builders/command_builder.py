from collections.abc import Callable
from typing import Any

from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_glue_core.common.operations.mutations.data import DeleteData
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateData

from amsdal_glue_connections.sql.sql_builders.operator_constructor import default_operator_constructor
from amsdal_glue_connections.sql.sql_builders.query_builder import build_conditions


def build_sql_data_command(  # noqa: PLR0913
    mutation: DataMutation,
    value_placeholder: str = '?',
    field_separator: str = '__',
    table_separator: str = '.',
    operator_constructor: Callable[
        [str, FieldLookup, FieldReference | Value, str, str, str, str, str, str],
        tuple[str, list[Any]],
    ] = default_operator_constructor,
    table_quote: str = '',
    field_quote: str = '',
) -> tuple[str, list[Any]]:
    if isinstance(mutation, InsertData):
        return _build_sql_insert_data(
            mutation,
            value_placeholder,
            field_separator,
            table_separator,
            operator_constructor,
            table_quote=table_quote,
            field_quote=field_quote,
        )

    if isinstance(mutation, UpdateData):
        return _build_sql_update_data(
            mutation,
            value_placeholder,
            field_separator,
            table_separator,
            operator_constructor,
            table_quote=table_quote,
            field_quote=field_quote,
        )

    if isinstance(mutation, DeleteData):
        return _build_sql_delete_data(
            mutation,
            value_placeholder,
            field_separator,
            table_separator,
            operator_constructor,
            table_quote=table_quote,
            field_quote=field_quote,
        )

    msg = f'Unsupported command type: {type(mutation)}'
    raise NotImplementedError(msg)


def _build_sql_insert_data(  # noqa: PLR0913
    command: InsertData,
    value_placeholder: str,
    field_separator: str,  # noqa: ARG001
    table_separator: str,  # noqa: ARG001
    operator_constructor: Callable[  # noqa: ARG001
        [str, FieldLookup, FieldReference | Value, str, str, str, str, str, str],
        tuple[str, list[Any]],
    ],
    table_quote: str = '',
    field_quote: str = '',  # noqa: ARG001
) -> tuple[str, list[Any]]:
    stmt = f'INSERT INTO {table_quote}{command.schema.name}{table_quote}'

    if not command.data:
        msg = 'No data provided for insert operation'
        raise ValueError(msg)

    values: list[Any] = []

    keys = sorted({key for data in command.data for key in data.data})
    placeholders = [[value_placeholder] * len(keys)] * len(command.data)

    if command.data:
        stmt += ' ('
        stmt += ', '.join(keys)
        stmt += ') VALUES '
        stmt += ', '.join(f'({", ".join(row)})' for row in placeholders)
        values.extend(data.data.get(key) for data in command.data for key in keys)

    return stmt, values


def _build_sql_update_data(  # noqa: PLR0913
    command: UpdateData,
    value_placeholder: str,
    field_separator: str,
    table_separator: str,
    operator_constructor: Callable[
        [str, FieldLookup, FieldReference | Value, str, str, str, str, str, str],
        tuple[str, list[Any]],
    ],
    table_quote: str = '',
    field_quote: str = '',
) -> tuple[str, list[Any]]:
    stmt = f'UPDATE {command.schema.name}'

    if command.schema.alias:
        stmt += f' AS {command.schema.alias}'

    if not command.data:
        msg = 'No data provided for update operation'
        raise ValueError(msg)

    values: list[Any] = []

    keys = sorted(set(command.data.data))

    if command.data:
        stmt += ' SET '
        stmt += ', '.join(f'{field_quote}{key}{field_quote} = {value_placeholder}' for key in keys)
        values.extend(command.data.data.get(key) for key in keys)

    if command.query:
        where, where_values = build_conditions(
            conditions=command.query,
            value_placeholder=value_placeholder,
            field_separator=field_separator,
            table_separator=table_separator,
            operator_constructor=operator_constructor,
            table_quote=table_quote,
            field_quote=field_quote,
        )

        stmt += f' WHERE {where}'
        values.extend(where_values)

    return stmt, values


def _build_sql_delete_data(  # noqa: PLR0913
    command: DeleteData,
    value_placeholder: str,
    field_separator: str,
    table_separator: str,
    operator_constructor: Callable[
        [str, FieldLookup, FieldReference | Value, str, str, str, str, str, str],
        tuple[str, list[Any]],
    ],
    table_quote: str = '',
    field_quote: str = '',
) -> tuple[str, list[Any]]:
    stmt = f'DELETE FROM {table_quote}{command.schema.name}{table_quote}'  # noqa: S608

    if command.schema.alias:
        stmt += f' AS {command.schema.alias}'

    values = []

    if command.query:
        where, where_values = build_conditions(
            conditions=command.query,
            value_placeholder=value_placeholder,
            field_separator=field_separator,
            table_separator=table_separator,
            operator_constructor=operator_constructor,
            table_quote=table_quote,
            field_quote=field_quote,
        )

        stmt += f' WHERE {where}'
        values.extend(where_values)

    return stmt, values
