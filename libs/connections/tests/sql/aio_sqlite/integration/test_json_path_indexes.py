"""JSON-path (expression) indexes on SQLite (async): created from a ``RegisterSchema`` and read back equal."""

import pytest
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import AddIndex
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY
from tests.sql.json_path_index_cases import INDEXES
from tests.sql.json_path_index_cases import TABLE
from tests.sql.json_path_index_cases import table_schema

_REF = SchemaReference(name=TABLE, version=Version.LATEST)


async def _introspect(connection: AsyncSqliteConnection) -> dict[str, IndexSchema]:
    query = QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
    schemas = await connection.query_schema(query)
    schema = next(s for s in schemas if s.name == TABLE)
    return {index.name: index for index in schema.indexes or []}


@pytest.mark.parametrize('case', list(INDEXES))
async def test_index_in_register_schema_round_trips(database_connection: AsyncSqliteConnection, case: str) -> None:
    declared = INDEXES[case]
    await database_connection.run_schema_command(
        SchemaCommand(mutations=[RegisterSchema(schema_ref=_REF, schema=table_schema([declared]))]),
    )

    introspected = await _introspect(database_connection)
    assert introspected == {declared.name: declared}
    assert [(f.name, f.json_path, f.output_type, f.direction) for f in introspected[declared.name].fields] == [
        (f.name, f.json_path, f.output_type, f.direction) for f in declared.fields
    ]


@pytest.mark.parametrize('case', list(INDEXES))
async def test_add_index_on_existing_table_round_trips(database_connection: AsyncSqliteConnection, case: str) -> None:
    declared = INDEXES[case]
    await database_connection.run_schema_command(
        SchemaCommand(mutations=[RegisterSchema(schema_ref=_REF, schema=table_schema())]),
    )
    await database_connection.run_schema_command(SchemaCommand(mutations=[AddIndex(schema_ref=_REF, index=declared)]))

    assert await _introspect(database_connection) == {declared.name: declared}


async def test_all_indexes_together_round_trip(database_connection: AsyncSqliteConnection) -> None:
    declared = list(INDEXES.values())
    await database_connection.run_schema_command(
        SchemaCommand(mutations=[RegisterSchema(schema_ref=_REF, schema=table_schema(declared))]),
    )

    assert await _introspect(database_connection) == {index.name: index for index in declared}
