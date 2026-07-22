"""Round-trip: case-sensitive text-match lookups are case-sensitive on SQLite.

SQLite `LIKE` is case-INsensitive for ASCII, so before the `glob(...)` lowering
`startswith='Test'` wrongly matched `'test2'`. These tests drive the real connection
against a live SQLite file and assert the actual rows returned.
"""

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

_NAME = 'TextMatchTable'


def _setup(connection: SqliteConnection) -> SchemaReference:
    schema = Schema(
        name=_NAME,
        version=Version.LATEST,
        properties=[PropertySchema(name='name', type=ScalarType.TEXT, required=True)],
    )
    connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema_ref=SchemaReference(name=_NAME, version=Version.LATEST),
                    schema=schema,
                ),
            ],
        ),
    )
    ref = SchemaReference(name=_NAME, version=Version.LATEST)
    connection.run_mutations(
        [
            InsertData(
                schema=ref,
                data=[DataInput(data={'name': 'Test2'}), DataInput(data={'name': 'test2'})],
            ),
        ]
    )
    return ref


def _names(connection: SqliteConnection, ref: SchemaReference, lookup: FieldLookup, value: str) -> set[str]:
    query = QueryStatement(
        table=ref,
        where=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='name'), table_name=_NAME),
                ),
                lookup=lookup,
                right=Value(value=value),
            ),
        ),
    )
    return {row.data['name'] for row in connection.query(query)}


def test_startswith_is_case_sensitive(database_connection: SqliteConnection) -> None:
    ref = _setup(database_connection)
    assert _names(database_connection, ref, FieldLookup.STARTSWITH, 'Test') == {'Test2'}


def test_istartswith_is_case_insensitive(database_connection: SqliteConnection) -> None:
    ref = _setup(database_connection)
    assert _names(database_connection, ref, FieldLookup.ISTARTSWITH, 'Test') == {'Test2', 'test2'}


def test_contains_is_case_sensitive(database_connection: SqliteConnection) -> None:
    ref = _setup(database_connection)
    assert _names(database_connection, ref, FieldLookup.CONTAINS, 'Test') == {'Test2'}


def test_icontains_is_case_insensitive(database_connection: SqliteConnection) -> None:
    ref = _setup(database_connection)
    assert _names(database_connection, ref, FieldLookup.ICONTAINS, 'test') == {'Test2', 'test2'}


def test_endswith_is_case_sensitive(database_connection: SqliteConnection) -> None:
    ref = _setup(database_connection)
    # 'Test2' and 'test2' both end in '2'; only 'st2' with matching case for the S is 'test2'.
    assert _names(database_connection, ref, FieldLookup.ENDSWITH, 'est2') == {'Test2', 'test2'}
    assert _names(database_connection, ref, FieldLookup.ENDSWITH, 'Test2') == {'Test2'}
