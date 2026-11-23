"""JSON-typed plain scalars in a JSON / JSONB column on SQLite (AMS-337, AMS-364).

``Value(x, output_type=JSONB)`` is how a caller says "this is a JSON value" -- PostgreSQL needs it to
store a string, number or boolean in a ``jsonb`` column at all. SQLite has no JSON type, and every
row written before callers typed their values holds the scalar as is. So on SQLite a JSON-typed plain
scalar is stored and compared like a bare value: inserts and updates store the native value, and a
whole-column filter compares it raw (``col = ?``), never through ``jsonb()``, which fails the whole
query on any row whose text is not JSON. Objects and arrays keep their JSON form.

The one exception is a string SQLite would not give back as written (AMS-364). A JSON column has
NUMERIC affinity, so SQLite stores the text ``'123'`` as the integer ``123``. A string that
starts with ``"`` is stored as JSON text too, so that reading decodes only what was stored that way. Such
a string is stored as its JSON text (``'"123"'``), filters compare it in that form, and reading decodes it
back to the string.
"""

import json
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

# Values a JSON column stores as written: the typed form is stored exactly like the bare one.
STORED_AS_IS: list[Any] = [
    'closed_won',
    'true',
    'null',
    '',
    'Inf',
    'Infinity',
    '0x1A',
    '1_000',
    'x"',
    5,
    2.5,
    True,
    False,
]
STORED_AS_IS_IDS = [
    'string',
    'true-string',
    'null-string',
    'empty-string',
    'inf-string',
    'infinity-string',
    'hex-string',
    'underscored-number-string',
    'trailing-quote-string',
    'int',
    'float',
    'true',
    'false',
]

# Strings stored as JSON text: SQLite turns the numeric-looking ones into numbers (NUMERIC affinity), and
# one starting with `"` would be taken for JSON text on read.
STORED_AS_JSON_TEXT: list[str] = [
    '123',
    ' 7 ',
    '+5',
    '.5',
    '5.',
    '1e5',
    '1E+5',
    '0005.500',
    '-0',
    '1e400',
    '"quoted"',
    '"',
]
STORED_AS_JSON_TEXT_IDS = [
    'integer-string',
    'integer-string-with-spaces',
    'signed-integer-string',
    'leading-dot-string',
    'trailing-dot-string',
    'exponent-string',
    'upper-exponent-string',
    'zero-padded-real-string',
    'negative-zero-string',
    'overflowing-real-string',
    'json-looking-string',
    'single-quote-char-string',
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


def _read(connection: SqliteConnection) -> dict[int, Any]:
    return {row.data['id']: row.data['payload'] for row in connection.query(QueryStatement(table=_REF))}


@pytest.mark.parametrize('value', STORED_AS_IS, ids=STORED_AS_IS_IDS)
def test_json_typed_scalar_is_stored_like_a_bare_value(database_connection: SqliteConnection, value: Any) -> None:
    """Inserting a JSON-typed plain scalar that SQLite keeps as written stores exactly what inserting the
    bare value stores -- same value, same SQLite storage class -- and both read back the same."""
    _register(database_connection)
    _insert(database_connection, 1, value)
    _insert(database_connection, 2, _json(value))

    assert _stored(database_connection, 2) == _stored(database_connection, 1)
    read = _read(database_connection)
    assert read[2] == read[1] == value


@pytest.mark.parametrize('value', STORED_AS_JSON_TEXT, ids=STORED_AS_JSON_TEXT_IDS)
def test_json_typed_string_sqlite_would_change_is_stored_as_json_text(
    database_connection: SqliteConnection, value: str
) -> None:
    """A JSON-typed string that SQLite would not give back as written is stored as its JSON text, and
    reads back as the same string, not as a number or the decoded inner text."""
    _register(database_connection)
    _insert(database_connection, 1, _json(value))

    assert _stored(database_connection, 1) == (json.dumps(value), 'text')
    assert _read(database_connection)[1] == value


@pytest.mark.parametrize(
    'value',
    [1 / 3, 1e20, 2**62, -0.5, float('inf'), b'\x00\xff', 'closed_won', '', '"closed_won"'],
    ids=['third', 'large-real', 'large-int', 'negative-real', 'infinity', 'blob', 'string', 'empty', 'quoted-string'],
)
def test_bare_value_in_a_json_column_reads_back_unchanged(database_connection: SqliteConnection, value: Any) -> None:
    """A value written bare reads back as stored: a number keeps its type and precision, a blob stays bytes,
    a text stays text."""
    _register(database_connection)
    database_connection.execute('INSERT INTO "doc" ("id", "payload") VALUES (?, ?)', 1, value)

    read = _read(database_connection)[1]

    assert read == value
    assert type(read) is type(value)


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


def test_filter_by_numeric_looking_string_matches_the_string_not_the_number(
    database_connection: SqliteConnection,
) -> None:
    """A whole-column filter with the JSON-typed string ``'123'`` matches the row holding that string and
    not the row holding the number ``123``, and the other way round."""
    _register(database_connection)
    _insert(database_connection, 1, _json('123'))
    _insert(database_connection, 2, _json(123))

    assert _ids_where_payload_equals(database_connection, _json('123')) == [1]
    assert _ids_where_payload_equals(database_connection, _json(123)) == [2]


def test_in_filter_with_numeric_looking_strings_matches_the_strings(database_connection: SqliteConnection) -> None:
    """An ``in`` filter whose candidates include a numeric-looking string matches the row holding that
    string, and the plain candidates as before."""
    _register(database_connection)
    _insert(database_connection, 1, _json('123'))
    _insert(database_connection, 2, _json(123))
    _insert(database_connection, 3, _json('closed_won'))

    query = QueryStatement(
        table=_REF,
        where=Conditions(
            Condition(
                left=_payload_ref(),
                lookup=FieldLookup.IN,
                right=Value(['123', 'closed_won'], output_type=ScalarType.JSONB),
            ),
        ),
    )

    assert sorted(row.data['id'] for row in database_connection.query(query)) == [1, 3]


@pytest.mark.parametrize(
    ('lookup', 'expected'),
    [(FieldLookup.GT, [2]), (FieldLookup.GTE, [1, 2]), (FieldLookup.LT, []), (FieldLookup.LTE, [1])],
    ids=['gt', 'gte', 'lt', 'lte'],
)
def test_range_filter_by_numeric_looking_string_compares_the_strings(
    database_connection: SqliteConnection, lookup: FieldLookup, expected: list[int]
) -> None:
    """A range filter with a numeric-looking JSON-typed string compares it with the stored strings of the
    same kind, as text."""
    _register(database_connection)
    _insert(database_connection, 1, _json('111'))
    _insert(database_connection, 2, _json('222'))

    query = QueryStatement(
        table=_REF,
        where=Conditions(Condition(left=_payload_ref(), lookup=lookup, right=_json('111'))),
    )

    assert sorted(row.data['id'] for row in database_connection.query(query)) == expected


def test_update_with_numeric_looking_string_reads_back_the_string(database_connection: SqliteConnection) -> None:
    """Updating a row with the JSON-typed string ``'123'`` stores its JSON text, so it reads back as the
    string."""
    _register(database_connection)
    _insert(database_connection, 1, _json('before'))

    database_connection.run_mutations(
        [UpdateData(schema=_REF, data=DataInput(data={'id': 1, 'payload': _json('123')}))]
    )

    assert _stored(database_connection, 1) == ('"123"', 'text')
    assert _read(database_connection)[1] == '123'
