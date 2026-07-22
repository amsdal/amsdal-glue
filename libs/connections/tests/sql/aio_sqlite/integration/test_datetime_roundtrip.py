from datetime import date
from datetime import datetime

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
                            PropertySchema(name='created_at', type=ScalarType.TIMESTAMP, required=True),
                            PropertySchema(name='event_day', type=ScalarType.DATE, required=True),
                        ],
                    ),
                ),
            ],
        ),
    )
    return SchemaReference(name='event', version=Version.LATEST)


@pytest.mark.asyncio
async def test_datetime_and_date_round_trip_as_python_objects(database_connection: AsyncSqliteConnection) -> None:
    schema_ref = await _register_event(database_connection)

    created_at = datetime(2020, 1, 2, 3, 4, 5)  # noqa: DTZ001
    event_day = date(2020, 1, 2)

    await database_connection.run_mutations([
        InsertData(
            schema=schema_ref,
            data=[DataInput(data={'id': 1, 'created_at': created_at, 'event_day': event_day})],
        ),
    ])

    result = await database_connection.query(QueryStatement(table=schema_ref))
    assert len(result) == 1
    row = result[0].data

    # The read-back converters must re-hydrate DATE/TIMESTAMP into Python objects,
    # not leave them as ISO strings.
    assert isinstance(row['created_at'], datetime)
    assert row['created_at'] == created_at
    assert isinstance(row['event_day'], date)
    assert not isinstance(row['event_day'], datetime)
    assert row['event_day'] == event_day
