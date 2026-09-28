"""Async mirror of the sync Postgres vector-index tests (`tests/sql/postgres/integration/test_vector_indexes.py`).

The custom-access-method introspection change (`_resolve_index_type` / `TABLE_INDEX_REGISTRY`) sits
in the shared `SchemaAssemblyMixin`, but every other Postgres integration module has a mirror under
this `aio_postgres` tree -- without one here, the async path stays untested for custom access methods,
declared-vs-introspected equality, storage-parameter round-tripping, and the default-opclass /
case-fold introspection fixes.
"""

from collections.abc import AsyncGenerator

import pytest
from amsdal_glue_core.common.data_models.indexes import CustomIndexType
from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import AddIndex

from amsdal_glue_connections.sql.connections.postgres_connection import AsyncPostgresConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY

_TABLE = 'documents'


@pytest.fixture
async def vector_connection(
    database_connection: AsyncPostgresConnection,
) -> AsyncGenerator[AsyncPostgresConnection, None]:
    try:
        await database_connection.execute('CREATE EXTENSION IF NOT EXISTS vector')
    except ConnectionError as exc:
        pytest.skip(f'pgvector extension unavailable on the test server: {exc}')

    await database_connection.execute(
        f'CREATE TABLE "{_TABLE}" (id SERIAL PRIMARY KEY, embedding VECTOR(3), title TEXT, body TEXT)'
    )
    yield database_connection


async def _add_index(connection: AsyncPostgresConnection, index: IndexSchema) -> None:
    await connection.run_schema_command(
        SchemaCommand(
            mutations=[
                AddIndex(schema_ref=SchemaReference(name=_TABLE, version=Version.LATEST), index=index),
            ],
        ),
    )


async def _introspect_indexes(connection: AsyncPostgresConnection) -> dict[str, IndexSchema]:
    query = QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
    schemas = await connection.query_schema(query)
    schema = next(s for s in schemas if s.name == _TABLE)
    return {index.name: index for index in schema.indexes or []}


async def test_hnsw_index_create_and_introspect(vector_connection: AsyncPostgresConnection) -> None:
    declared = IndexSchema(
        name='idx_documents_embedding_hnsw',
        fields=[IndexField(name='embedding', op_class='vector_cosine_ops')],
        index_type=CustomIndexType(name='hnsw'),
        parameters={'m': '16', 'ef_construction': '64'},
    )
    await _add_index(vector_connection, declared)

    introspected = (await _introspect_indexes(vector_connection))[declared.name]
    assert introspected.index_type == CustomIndexType(name='hnsw')
    assert introspected.unique is False
    expected_field = IndexField(name='embedding', direction=OrderDirection.ASC, op_class='vector_cosine_ops')
    assert introspected.fields == [expected_field]
    assert introspected.parameters == {'m': '16', 'ef_construction': '64'}
    assert declared == introspected


async def test_ivfflat_index_create_and_introspect(vector_connection: AsyncPostgresConnection) -> None:
    declared = IndexSchema(
        name='idx_documents_embedding_ivfflat',
        fields=[IndexField(name='embedding', op_class='vector_cosine_ops')],
        index_type=CustomIndexType(name='ivfflat'),
        parameters={'lists': '10'},
    )
    await _add_index(vector_connection, declared)

    introspected = (await _introspect_indexes(vector_connection))[declared.name]
    assert introspected.index_type == CustomIndexType(name='ivfflat')
    assert introspected.unique is False
    expected_field = IndexField(name='embedding', direction=OrderDirection.ASC, op_class='vector_cosine_ops')
    assert introspected.fields == [expected_field]
    assert introspected.parameters == {'lists': '10'}
    assert declared == introspected


async def test_declared_index_equals_introspected_custom_am_and_op_class(
    vector_connection: AsyncPostgresConnection,
) -> None:
    declared = IndexSchema(
        name='idx_documents_embedding_hnsw_eq',
        fields=[IndexField(name='embedding', op_class='vector_cosine_ops')],
        index_type=CustomIndexType(name='hnsw'),
    )
    await _add_index(vector_connection, declared)

    introspected = (await _introspect_indexes(vector_connection))[declared.name]
    assert declared == introspected
    assert introspected.index_type == CustomIndexType(name='hnsw')


async def test_declared_index_equals_introspected_include_columns(vector_connection: AsyncPostgresConnection) -> None:
    declared = IndexSchema(
        name='idx_documents_title_include_body',
        fields=[IndexField(name='title')],
        include=['body'],
    )
    await _add_index(vector_connection, declared)

    introspected = (await _introspect_indexes(vector_connection))[declared.name]
    assert declared == introspected
    assert introspected.include == ['body']


async def test_declared_index_equals_introspected_desc_field(vector_connection: AsyncPostgresConnection) -> None:
    declared = IndexSchema(
        name='idx_documents_title_desc',
        fields=[IndexField(name='title', direction=OrderDirection.DESC)],
    )
    await _add_index(vector_connection, declared)

    introspected = (await _introspect_indexes(vector_connection))[declared.name]
    assert declared == introspected
    assert introspected.fields[0].direction == OrderDirection.DESC


async def test_custom_type_name_case_round_trip(vector_connection: AsyncPostgresConnection) -> None:
    declared = IndexSchema(
        name='idx_documents_embedding_hnsw_case',
        fields=[IndexField(name='embedding', op_class='vector_cosine_ops')],
        index_type=CustomIndexType(name='HNSW'),
    )
    await _add_index(vector_connection, declared)

    introspected = (await _introspect_indexes(vector_connection))[declared.name]
    assert introspected.index_type == CustomIndexType(name='hnsw')
    assert declared == introspected


async def test_btree_default_op_class_round_trip(vector_connection: AsyncPostgresConnection) -> None:
    declared = IndexSchema(
        name='idx_documents_title_text_ops',
        fields=[IndexField(name='title', op_class='text_ops')],
    )
    await _add_index(vector_connection, declared)

    introspected = (await _introspect_indexes(vector_connection))[declared.name]
    assert introspected.fields[0].op_class is None
    assert introspected.fields[0].default_op_class == 'text_ops'
    assert declared == introspected
