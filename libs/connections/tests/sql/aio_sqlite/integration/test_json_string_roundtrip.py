"""A JSON-typed string that SQLite would change reads back unchanged through the async connection (AMS-364).

The sync suite (``sqlite_connection/integration/test_json_column_roundtrip.py``) covers the cases; this
checks that the async connection reads a JSON column with the same converter.
"""

import pytest
from amsdal_glue_core.common.data_models.data import DataInput
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection

_REF = SchemaReference(name='doc', version=Version.LATEST)


@pytest.mark.parametrize('value', ['123', '"quoted"', 'closed_won'], ids=['numeric-string', 'quoted-string', 'string'])
async def test_json_typed_string_reads_back_unchanged(database_connection: AsyncSqliteConnection, value: str) -> None:
    """A JSON-typed string saved through the async connection reads back as the same string, including
    one SQLite would otherwise turn into a number or decode."""
    await database_connection.run_schema_command(
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
    await database_connection.run_mutations(
        [
            InsertData(
                schema=_REF,
                data=[DataInput(data={'id': 1, 'payload': Value(value, output_type=ScalarType.JSONB)})],
            )
        ]
    )

    rows = await database_connection.query(QueryStatement(table=_REF))

    assert rows[0].data['payload'] == value
