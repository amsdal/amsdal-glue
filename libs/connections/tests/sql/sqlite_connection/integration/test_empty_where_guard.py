"""Guard against UPDATE/DELETE mutations built with effectively-empty WHERE conditions.

An empty ``Conditions()`` (or a nested-only-empty ``Conditions(Conditions())``) used as the
``query`` of ``UpdateData`` / ``DeleteData`` previously produced broken SQL with a dangling
``WHERE`` and no predicate. That is a destructive footgun: silently rendering no WHERE would
turn the mistake into an ALL-ROWS update/delete. The Rust SQL generator must instead reject it
at compile time with a clear ``ValueError`` that points the caller at ``query=None``.

``query=None`` remains legitimate (intentional all-rows) and must keep working, as must a real
``Conditions(Condition(...))`` predicate.
"""

import pytest
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.data import DeleteData
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection


def _setup_table(connection: SqliteConnection) -> Schema:
    schema: Schema = connection.run_schema_command(  # type: ignore[assignment]
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema_ref=SchemaReference(name='TestTable', version=Version.LATEST),
                    schema=Schema(
                        name='TestTable',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(name='field_a', type=ScalarType.TEXT, required=False),
                            PropertySchema(name='field_b', type=ScalarType.INTEGER, required=False),
                        ],
                    ),
                ),
            ],
        ),
    )[0]
    connection.run_mutations(
        [
            InsertData(
                schema=SchemaReference(name=schema.name, version=schema.version),
                data=[
                    Data(data={'field_a': 'value1', 'field_b': 1}),
                    Data(data={'field_a': 'value2', 'field_b': 2}),
                ],
            ),
        ]
    )
    return schema


def _read_rows(connection: SqliteConnection, schema: Schema) -> list[dict]:
    result = connection.query(
        QueryStatement(table=SchemaReference(name=schema.name, version=schema.version)),
    )
    return [data.data for data in result]


def _b_equals_1(schema: Schema) -> Condition:
    return Condition(
        left=FieldReferenceExpression(
            field_reference=FieldReference(field=Field(name='field_b'), table_name=schema.name),
        ),
        lookup=FieldLookup.EQ,
        right=Value(value=1),
    )


# ---------------------------------------------------------------------------
# UPDATE — effectively-empty WHERE must raise, not touch any row
# ---------------------------------------------------------------------------


def test_update_empty_conditions_raises(database_connection: SqliteConnection) -> None:
    schema = _setup_table(database_connection)

    with pytest.raises(ValueError) as exc_info:
        database_connection.run_mutations(
            [
                UpdateData(
                    schema=SchemaReference(name=schema.name, version=schema.version),
                    data={'field_a': Value(value='mutated')},
                    query=Conditions(),
                ),
            ]
        )

    assert 'all rows' in str(exc_info.value)
    assert 'query=None' in str(exc_info.value)
    # No row must have been changed.
    assert _read_rows(database_connection, schema) == [
        {'field_a': 'value1', 'field_b': 1},
        {'field_a': 'value2', 'field_b': 2},
    ]


def test_update_nested_empty_conditions_raises(database_connection: SqliteConnection) -> None:
    schema = _setup_table(database_connection)

    with pytest.raises(ValueError) as exc_info:
        database_connection.run_mutations(
            [
                UpdateData(
                    schema=SchemaReference(name=schema.name, version=schema.version),
                    data={'field_a': Value(value='mutated')},
                    query=Conditions(Conditions()),
                ),
            ]
        )

    assert 'all rows' in str(exc_info.value)
    assert 'query=None' in str(exc_info.value)
    assert _read_rows(database_connection, schema) == [
        {'field_a': 'value1', 'field_b': 1},
        {'field_a': 'value2', 'field_b': 2},
    ]


# ---------------------------------------------------------------------------
# DELETE — effectively-empty WHERE must raise, not delete any row
# ---------------------------------------------------------------------------


def test_delete_empty_conditions_raises(database_connection: SqliteConnection) -> None:
    schema = _setup_table(database_connection)

    with pytest.raises(ValueError) as exc_info:
        database_connection.run_mutations(
            [
                DeleteData(
                    schema=SchemaReference(name=schema.name, version=schema.version),
                    query=Conditions(),
                ),
            ]
        )

    assert 'all rows' in str(exc_info.value)
    assert 'query=None' in str(exc_info.value)
    assert _read_rows(database_connection, schema) == [
        {'field_a': 'value1', 'field_b': 1},
        {'field_a': 'value2', 'field_b': 2},
    ]


def test_delete_nested_empty_conditions_raises(database_connection: SqliteConnection) -> None:
    schema = _setup_table(database_connection)

    with pytest.raises(ValueError) as exc_info:
        database_connection.run_mutations(
            [
                DeleteData(
                    schema=SchemaReference(name=schema.name, version=schema.version),
                    query=Conditions(Conditions()),
                ),
            ]
        )

    assert 'all rows' in str(exc_info.value)
    assert 'query=None' in str(exc_info.value)
    assert _read_rows(database_connection, schema) == [
        {'field_a': 'value1', 'field_b': 1},
        {'field_a': 'value2', 'field_b': 2},
    ]


# ---------------------------------------------------------------------------
# Regression — legitimate all-rows (query=None) and real conditions still work
# ---------------------------------------------------------------------------


def test_update_query_none_affects_all_rows(database_connection: SqliteConnection) -> None:
    schema = _setup_table(database_connection)

    database_connection.run_mutations(
        [
            UpdateData(
                schema=SchemaReference(name=schema.name, version=schema.version),
                data={'field_a': Value(value='all')},
                query=None,
            ),
        ]
    )

    assert _read_rows(database_connection, schema) == [
        {'field_a': 'all', 'field_b': 1},
        {'field_a': 'all', 'field_b': 2},
    ]


def test_update_real_condition_affects_matching_only(database_connection: SqliteConnection) -> None:
    schema = _setup_table(database_connection)

    database_connection.run_mutations(
        [
            UpdateData(
                schema=SchemaReference(name=schema.name, version=schema.version),
                data={'field_a': Value(value='only1')},
                query=Conditions(_b_equals_1(schema)),
            ),
        ]
    )

    assert _read_rows(database_connection, schema) == [
        {'field_a': 'only1', 'field_b': 1},
        {'field_a': 'value2', 'field_b': 2},
    ]


def test_delete_query_none_deletes_all_rows(database_connection: SqliteConnection) -> None:
    schema = _setup_table(database_connection)

    database_connection.run_mutations(
        [
            DeleteData(
                schema=SchemaReference(name=schema.name, version=schema.version),
                query=None,
            ),
        ]
    )

    assert _read_rows(database_connection, schema) == []


def test_delete_real_condition_deletes_matching_only(database_connection: SqliteConnection) -> None:
    schema = _setup_table(database_connection)

    database_connection.run_mutations(
        [
            DeleteData(
                schema=SchemaReference(name=schema.name, version=schema.version),
                query=Conditions(_b_equals_1(schema)),
            ),
        ]
    )

    assert _read_rows(database_connection, schema) == [
        {'field_a': 'value2', 'field_b': 2},
    ]
