from collections.abc import Callable
from typing import Any

from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_glue_core.common.operations.mutations.data import DeleteData
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateData

from amsdal_glue_connections.sql.sql_builders.nested_field_transform import default_nested_field_transform
from amsdal_glue_connections.sql.sql_builders.operator_constructor import default_operator_constructor
from amsdal_glue_connections.sql.sql_builders.query_builder import build_conditions


def build_sql_data_command(  # noqa: PLR0913
    mutation: DataMutation,
    value_placeholder: str = '?',
    table_separator: str = '.',
    operator_constructor: Callable[
        [
            str,
            FieldLookup,
            FieldReference | Value,
            str,
            str,
            str,
            str,
            str,
            Callable[[Any], Any],
            Callable[[str, str, list[str], Any, str, str, str], str],
        ],
        tuple[str, list[Any]],
    ] = default_operator_constructor,
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: Callable[[str, str, list[str], Any, str, str, str], str] = default_nested_field_transform,
) -> tuple[str, list[Any]]:
    """
    Builds an SQL command for the given data mutation.

    Args:
        mutation (DataMutation): The data mutation to be converted to an SQL command.
        value_placeholder (str, optional): The placeholder for values in the SQL command. Defaults to '?'.
        table_separator (str, optional): The separator for table names. Defaults to '.'.
        operator_constructor (Callable, optional): The function to construct operators.
                                                   Defaults to default_operator_constructor.
        table_quote (str, optional): The quote character for table names. Defaults to ''.
        field_quote (str, optional): The quote character for field names. Defaults to ''.
        value_transform (Callable, optional): The function to transform values. Defaults to lambda x: x.
        nested_field_transform (Callable, optional): The function to transform nested fields.
                                                     Defaults to default_nested_field_transform.

    Returns:
        tuple[str, list[Any]]: The SQL command and the list of values.
    """
    if isinstance(mutation, InsertData):
        return _build_sql_insert_data(
            mutation,
            value_placeholder,
            table_quote=table_quote,
            field_quote=field_quote,
            value_transform=value_transform,
        )

    if isinstance(mutation, UpdateData):
        return _build_sql_update_data(
            mutation,
            value_placeholder,
            table_separator,
            operator_constructor,
            table_quote=table_quote,
            field_quote=field_quote,
            value_transform=value_transform,
            nested_field_transform=nested_field_transform,
        )

    if isinstance(mutation, DeleteData):
        return _build_sql_delete_data(
            mutation,
            value_placeholder,
            table_separator,
            operator_constructor,
            table_quote=table_quote,
            field_quote=field_quote,
            value_transform=value_transform,
            nested_field_transform=nested_field_transform,
        )

    msg = f'Unsupported command type: {type(mutation)}'
    raise NotImplementedError(msg)


def _build_sql_insert_data(
    command: InsertData,
    value_placeholder: str,
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
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
        stmt += ', '.join(f'{field_quote}{key}{field_quote}' for key in keys)
        stmt += ') VALUES '
        stmt += ', '.join(f'({", ".join(row)})' for row in placeholders)
        values.extend(value_transform(data.data.get(key)) for data in command.data for key in keys)

    return stmt, values


def _build_sql_update_data(  # noqa: PLR0913
    command: UpdateData,
    value_placeholder: str,
    table_separator: str,
    operator_constructor: Callable[
        [
            str,
            FieldLookup,
            FieldReference | Value,
            str,
            str,
            str,
            str,
            str,
            Callable[[Any], Any],
            Callable[[str, str, list[str], Any, str, str, str], str],
        ],
        tuple[str, list[Any]],
    ] = default_operator_constructor,
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: Callable[[str, str, list[str], Any, str, str, str], str] = default_nested_field_transform,
) -> tuple[str, list[Any]]:
    stmt = f'UPDATE {table_quote}{command.schema.name}{table_quote}'

    if command.schema.alias:
        stmt += f' AS {table_quote}{command.schema.alias}{table_quote}'

    if not command.data:
        msg = 'No data provided for update operation'
        raise ValueError(msg)

    values: list[Any] = []

    keys = sorted(set(command.data.data))

    if command.data:
        stmt += ' SET '
        stmt += ', '.join(f'{field_quote}{key}{field_quote} = {value_placeholder}' for key in keys)
        values.extend(value_transform(command.data.data.get(key)) for key in keys)

    if command.query:
        where, where_values = build_conditions(
            conditions=command.query,
            value_placeholder=value_placeholder,
            table_separator=table_separator,
            operator_constructor=operator_constructor,
            table_quote=table_quote,
            field_quote=field_quote,
            value_transform=value_transform,
            nested_field_transform=nested_field_transform,
        )

        stmt += f' WHERE {where}'
        values.extend(where_values)

    return stmt, values


def _build_sql_delete_data(  # noqa: PLR0913
    command: DeleteData,
    value_placeholder: str,
    table_separator: str,
    operator_constructor: Callable[
        [
            str,
            FieldLookup,
            FieldReference | Value,
            str,
            str,
            str,
            str,
            str,
            Callable[[Any], Any],
            Callable[[str, str, list[str], Any, str, str, str], str],
        ],
        tuple[str, list[Any]],
    ] = default_operator_constructor,
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: Callable[[str, str, list[str], Any, str, str, str], str] = default_nested_field_transform,
) -> tuple[str, list[Any]]:
    stmt = f'DELETE FROM {table_quote}{command.schema.name}{table_quote}'  # noqa: S608

    if command.schema.alias:
        stmt += f' AS {table_quote}{command.schema.alias}{table_quote}'

    values = []

    if command.query:
        where, where_values = build_conditions(
            conditions=command.query,
            value_placeholder=value_placeholder,
            table_separator=table_separator,
            operator_constructor=operator_constructor,
            table_quote=table_quote,
            field_quote=field_quote,
            value_transform=value_transform,
            nested_field_transform=nested_field_transform,
        )

        stmt += f' WHERE {where}'
        values.extend(where_values)
    return stmt, values
