"""JSON-typed plain scalars in a JSON / JSONB column on SQLite (AMS-337).

``Value(x, output_type=JSONB)`` is how a caller says "this is a JSON value" -- PostgreSQL needs it to
store a string, number or boolean in a ``jsonb`` column at all. SQLite has no JSON type, and every
row written before callers typed their values holds the scalar as is. So on SQLite a JSON-typed plain
scalar is stored and compared exactly like a bare value: inserts and updates store the native value,
and a whole-column filter compares it raw (``col = ?``), never through ``jsonb()``, which fails the
whole query on any row whose text is not JSON. Objects and arrays keep their JSON form.
"""

from typing import Any

import pytest
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import DataInput
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
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection

SCALARS: list[Any] = ['closed_won', '"quoted"', 'true', '123', '', 5, 2.5, True, False]
SCALAR_IDS = [
    'string',
    'json-looking-string',
    'true-string',
    'numeric-string',
    'empty-string',
    'int',
    'float',
    'true',
    'false',
]

_REF = SchemaReference(name='doc', version=Version.LATEST)


def _register(connection: SqliteConnection) -> None:
    connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema_ref=_REF,
                    schema=Schema(
                        name='doc',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                            PropertySchema(name='payload', type=ScalarType.JSONB, required=False),
                        ],
                    ),
                ),
            ],
        ),
    )


def _json(value: Any) -> Value:
    return Value(value, output_type=ScalarType.JSONB)


def _insert(connection: SqliteConnection, row_id: int, payload: Any) -> None:
    connection.run_mutations([InsertData(schema=_REF, data=[DataInput(data={'id': row_id, 'payload': payload})])])


def _stored(connection: SqliteConnection, row_id: int) -> tuple[Any, str]:
    """The stored value and its SQLite storage class."""
    cursor = connection.execute('SELECT "payload", typeof("payload") FROM "doc" WHERE "id" = ?', row_id)
    stored = cursor.fetchone()
    cursor.close()
    return stored[0], stored[1]


def _payload_ref() -> FieldReferenceExpression:
    return FieldReferenceExpression(field_reference=FieldReference(field=Field(name='payload'), table_name='doc'))


def _ids_where_payload_equals(connection: SqliteConnection, value: Any) -> list[int]:
    query = QueryStatement(
        table=_REF,
        where=Conditions(
            Condition(
                left=_payload_ref(),
                lookup=FieldLookup.EQ,
                right=value,
            ),
        ),
    )
    return sorted(row.data['id'] for row in connection.query(query))


@pytest.mark.parametrize('value', SCALARS, ids=SCALAR_IDS)
def test_json_typed_scalar_is_stored_like_a_bare_value(database_connection: SqliteConnection, value: Any) -> None:
    """Inserting a JSON-typed plain scalar stores exactly what inserting the bare value stores -- same
    value, same SQLite storage class -- and both read back the same."""
    _register(database_connection)
    _insert(database_connection, 1, value)
    _insert(database_connection, 2, _json(value))

    assert _stored(database_connection, 2) == _stored(database_connection, 1)
    read = {row.data['id']: row.data['payload'] for row in database_connection.query(QueryStatement(table=_REF))}
    assert read[2] == read[1]


def test_json_typed_scalar_in_an_update_is_stored_like_a_bare_value(database_connection: SqliteConnection) -> None:
    """Updating a row with a JSON-typed string stores the plain string, as an update with the bare
    string does."""
    _register(database_connection)
    _insert(database_connection, 1, 'before')

    database_connection.run_mutations(
        [UpdateData(schema=_REF, data=DataInput(data={'id': 1, 'payload': _json('after')}))]
    )

    assert _stored(database_connection, 1) == ('after', 'text')


@pytest.mark.parametrize('value', [{'b': 2, 'a': 1}, ['a', 1]], ids=['dict', 'list'])
def test_json_typed_container_is_still_stored_as_json(database_connection: SqliteConnection, value: Any) -> None:
    """An object or array is stored as JSON text and decoded on read, typed or not."""
    _register(database_connection)
    _insert(database_connection, 1, _json(value))

    _, storage_class = _stored(database_connection, 1)
    assert storage_class == 'text'
    assert database_connection.query(QueryStatement(table=_REF))[0].data['payload'] == value


@pytest.mark.parametrize('value', ['closed_won', 5, True], ids=['string', 'int', 'bool'])
def test_filter_by_json_typed_scalar_matches_old_and_new_rows(
    database_connection: SqliteConnection, value: Any
) -> None:
    """A whole-column filter with a JSON-typed scalar matches the row written bare (before values were
    typed) and the row written typed, and not the other rows."""
    _register(database_connection)
    _insert(database_connection, 1, value)  # written before JSON typing
    _insert(database_connection, 2, _json(value))  # written typed
    _insert(database_connection, 3, 'something else')

    assert _ids_where_payload_equals(database_connection, _json(value)) == [1, 2]


def test_filter_by_json_typed_scalar_ignores_rows_whose_text_is_not_json(database_connection: SqliteConnection) -> None:
    """A row holding text that is not JSON does not make a whole-column filter fail: the filter just
    does not match it."""
    _register(database_connection)
    _insert(database_connection, 1, 'not json at all')
    _insert(database_connection, 2, _json('closed_won'))

    assert _ids_where_payload_equals(database_connection, _json('closed_won')) == [2]


def test_filter_by_json_typed_object_still_compares_as_json(database_connection: SqliteConnection) -> None:
    """A whole-column filter with a JSON object still matches regardless of key spacing (the existing
    `jsonb()` normalisation for containers is unchanged)."""
    _register(database_connection)
    database_connection.execute('INSERT INTO "doc" ("id", "payload") VALUES (?, ?)', 1, '{"a": 1}')
    _insert(database_connection, 2, _json({'a': 2}))

    assert _ids_where_payload_equals(database_connection, _json({'a': 1})) == [1]


def test_in_filter_with_json_typed_scalars_matches_old_and_new_rows(database_connection: SqliteConnection) -> None:
    """An ``in`` filter whose candidates are JSON-typed scalars matches rows written bare and rows
    written typed, compared as plain values."""
    _register(database_connection)
    _insert(database_connection, 1, 'closed_won')  # written before JSON typing
    _insert(database_connection, 2, _json(5))  # written typed
    _insert(database_connection, 3, 'open')
    _insert(database_connection, 4, 'not json at all')

    in_typed = Value(['closed_won', 5], output_type=ScalarType.JSONB)
    query = QueryStatement(
        table=_REF,
        where=Conditions(
            Condition(
                left=_payload_ref(),
                lookup=FieldLookup.IN,
                right=in_typed,
            ),
        ),
    )

    assert sorted(row.data['id'] for row in database_connection.query(query)) == [1, 2]
