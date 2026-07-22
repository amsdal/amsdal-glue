"""Async twin of the SQLite TIMESTAMPTZ round-trip / read-back coverage."""

from datetime import datetime
from datetime import timezone

import pytest
from amsdal_glue_core.common.data_models.data import DataInput
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY


async def _register_event(database_connection: AsyncSqliteConnection) -> SchemaReference:
    await database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema_ref=SchemaReference(name='event', version=Version.LATEST),
                    schema=Schema(
                        name='event',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                            PropertySchema(name='created_at', type=ScalarType.TIMESTAMPTZ, required=True),
                        ],
                    ),
                ),
            ],
        ),
    )
    return SchemaReference(name='event', version=Version.LATEST)


@pytest.mark.asyncio
async def test_timestamptz_round_trips_and_reads_back_as_datetime(
    database_connection: AsyncSqliteConnection,
) -> None:
    schema_ref = await _register_event(database_connection)

    query = QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
    schema = next(s for s in await database_connection.query_schema(query) if s.name == 'event')
    created_type = next(p.type for p in schema.properties if p.name == 'created_at')
    assert created_type == ScalarType.TIMESTAMPTZ

    created_at = datetime(2020, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    await database_connection.run_mutations([
        InsertData(schema=schema_ref, data=[DataInput(data={'id': 1, 'created_at': created_at})]),
    ])

    result = await database_connection.query(QueryStatement(table=schema_ref))
    assert len(result) == 1
    row = result[0].data
    assert isinstance(row['created_at'], datetime)
    assert row['created_at'] == created_at
