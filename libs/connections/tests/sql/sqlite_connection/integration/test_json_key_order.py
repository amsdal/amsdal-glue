"""JSON object key order: ``_sql_core`` must preserve INSERTION order, not sort keys.

``serde_json::Map`` defaulted to a ``BTreeMap`` (alphabetically-sorted keys), so every JSON object the
generator reserialised came out key-sorted instead of insertion order. A whole-object
``filter(json_field={...})`` against a legacy insertion-order row then silently returned 0 rows.
Enabling serde_json's ``preserve_order`` feature backs the map with an ``IndexMap`` (insertion order),
restoring insertion-order output.

These tests drive a non-alphabetical dict ``{'b':2,'a':1,'m':13}`` through the generator and assert the
stored/bound JSON keeps ``b,a,m`` order (== ``json.dumps`` insertion order), not sorted ``a,b,m``. They
FAIL on the ``BTreeMap`` build and PASS after ``preserve_order``.
"""

import json

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
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection

# Non-alphabetical keys: insertion order (b, a, m) differs from sorted order (a, b, m).
_UNSORTED = {'b': 2, 'a': 1, 'm': 13}
_NESTED = {'ref': {'resource': 'sqlite-state', 'class_name': 'Post', 'object_id': 1}}


def _register(database_connection: SqliteConnection) -> SchemaReference:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema_ref=SchemaReference(name='Doc', version=Version.LATEST),
                    schema=Schema(
                        name='Doc',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                            PropertySchema(name='payload', type=ScalarType.JSONB, required=True),
                        ],
                    ),
                ),
            ],
        ),
    )
    return SchemaReference(name='Doc', version=Version.LATEST)


def _fref(name: str) -> FieldReferenceExpression:
    return FieldReferenceExpression(field_reference=FieldReference(field=Field(name=name), table_name='Doc'))


def _stored_json(database_connection: SqliteConnection, id_: int) -> str:
    cur = database_connection.execute('SELECT "payload" FROM "Doc" WHERE "id" = ?', id_)
    (value,) = cur.fetchone()
    cur.close()
    return value


def test_stored_json_preserves_insertion_order(database_connection: SqliteConnection) -> None:
    """A dict inserted through the generator (Rust serde_json) stores keys in insertion order."""
    schema_ref = _register(database_connection)

    database_connection.run_mutations(
        [
            InsertData(schema=schema_ref, data=[DataInput(data={'id': 1, 'payload': _UNSORTED})]),
        ]
    )

    # Insertion order b,a,m -- NOT sorted a,b,m -- byte-identical to json.dumps of the same dict.
    assert _stored_json(database_connection, 1) == json.dumps(_UNSORTED, separators=(',', ':'))
    assert _stored_json(database_connection, 1) == '{"b":2,"a":1,"m":13}'


def test_nested_object_preserves_insertion_order(database_connection: SqliteConnection) -> None:
    """The Reference shape's nested object also emits in insertion order."""
    schema_ref = _register(database_connection)

    database_connection.run_mutations(
        [
            InsertData(schema=schema_ref, data=[DataInput(data={'id': 1, 'payload': _NESTED})]),
        ]
    )

    assert _stored_json(database_connection, 1) == json.dumps(_NESTED, separators=(',', ':'))


def test_whole_object_filter_matches_insertion_order_row(database_connection: SqliteConnection) -> None:
    """A whole-object filter matches a row written with the same insertion order (0-row bug guard)."""
    schema_ref = _register(database_connection)

    # Seed a legacy insertion-order row (bare ? + json.dumps).
    database_connection.execute('INSERT INTO "Doc" ("id", "payload") VALUES (?, ?)', 1, json.dumps(_UNSORTED))
    # A decoy that must not match.
    database_connection.execute('INSERT INTO "Doc" ("id", "payload") VALUES (?, ?)', 2, json.dumps({'x': 9}))

    query = QueryStatement(
        table=schema_ref,
        where=Conditions(
            Condition(
                left=_fref('payload'),
                lookup=FieldLookup.EQ,
                right=Value(_UNSORTED, output_type=ScalarType.JSONB),
            ),
        ),
    )

    result = list(database_connection.query(query))
    assert [row.data['id'] for row in result] == [1]
