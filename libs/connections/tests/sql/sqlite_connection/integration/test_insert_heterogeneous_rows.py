"""A single multi-row INSERT emits one column list at the SQL level, so every row
must share the first row's exact column set. These tests prove heterogeneous rows are
rejected with a clear error (instead of silently NULL-filling missing columns or
dropping extra ones), while reordered-but-uniform rows still insert correctly.
"""

import pytest
from amsdal_glue_core.common.data_models.data import DataInput
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection


def _ref() -> SchemaReference:
    return SchemaReference(name='rows', version=Version.LATEST)


def _setup(connection: SqliteConnection) -> None:
    connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema_ref=_ref(),
                    schema=Schema(
                        name='rows',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                            PropertySchema(name='a', type=ScalarType.INTEGER, required=False),
                            PropertySchema(name='b', type=ScalarType.INTEGER, required=False),
                        ],
                    ),
                ),
            ],
        )
    )


def _read_all(connection: SqliteConnection) -> list[dict]:
    query = QueryStatement(
        table=_ref(),
        order_by=[
            OrderByQuery(
                expression=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='id'), table_name='rows')
                ),
                direction=OrderDirection.ASC,
            )
        ],
    )
    return [row.data for row in connection.query(query)]


def test_insert_second_row_missing_column_raises(database_connection: SqliteConnection) -> None:
    """Second row lacks 'b' present in the first: must raise, not silently insert NULL."""
    _setup(database_connection)

    with pytest.raises(ValueError) as exc_info:
        database_connection.run_mutations([
            InsertData(
                schema=_ref(),
                data=[
                    DataInput(data={'id': 1, 'a': 10, 'b': 20}),
                    DataInput(data={'id': 2, 'a': 30}),  # missing 'b'
                ],
            )
        ])

    message = str(exc_info.value)
    assert 'row 1' in message
    assert 'b' in message
    # Nothing should have been persisted.
    assert _read_all(database_connection) == []


def test_insert_second_row_extra_column_raises(database_connection: SqliteConnection) -> None:
    """Second row carries an extra 'b' absent from the first: must raise, not silently drop."""
    _setup(database_connection)

    with pytest.raises(ValueError) as exc_info:
        database_connection.run_mutations([
            InsertData(
                schema=_ref(),
                data=[
                    DataInput(data={'id': 1, 'a': 10}),
                    DataInput(data={'id': 2, 'a': 30, 'b': 99}),  # extra 'b'
                ],
            )
        ])

    message = str(exc_info.value)
    assert 'row 1' in message


def test_insert_uniform_rows_reordered_keys_ok(database_connection: SqliteConnection) -> None:
    """Same column set in a different key order still inserts, values in the right columns."""
    _setup(database_connection)

    database_connection.run_mutations([
        InsertData(
            schema=_ref(),
            data=[
                DataInput(data={'id': 1, 'a': 10, 'b': 20}),
                DataInput(data={'b': 40, 'id': 2, 'a': 30}),  # same keys, different order
            ],
        )
    ])

    assert _read_all(database_connection) == [
        {'id': 1, 'a': 10, 'b': 20},
        {'id': 2, 'a': 30, 'b': 40},
    ]
