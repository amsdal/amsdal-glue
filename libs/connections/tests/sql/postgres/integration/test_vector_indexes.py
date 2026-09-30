from collections.abc import Generator

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

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY

_TABLE = 'documents'


@pytest.fixture
def vector_connection(database_connection: PostgresConnection) -> Generator[PostgresConnection, None, None]:
    try:
        database_connection.execute('CREATE EXTENSION IF NOT EXISTS vector')
    except ConnectionError as exc:
        pytest.skip(f'pgvector extension unavailable on the test server: {exc}')

    database_connection.execute(
        f'CREATE TABLE "{_TABLE}" (id SERIAL PRIMARY KEY, embedding VECTOR(3), title TEXT, body TEXT)'
    )
    yield database_connection


def _add_index(connection: PostgresConnection, index: IndexSchema) -> None:
    connection.run_schema_command(
        SchemaCommand(
            mutations=[
                AddIndex(schema_ref=SchemaReference(name=_TABLE, version=Version.LATEST), index=index),
            ],
        ),
    )


def _introspect_indexes(connection: PostgresConnection) -> dict[str, IndexSchema]:
    query = QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
    schema = next(s for s in connection.query_schema(query) if s.name == _TABLE)
    return {index.name: index for index in schema.indexes or []}


def test_hnsw_index_create_and_introspect(vector_connection: PostgresConnection) -> None:
    declared = IndexSchema(
        name='idx_documents_embedding_hnsw',
        fields=[IndexField(name='embedding', op_class='vector_cosine_ops')],
        index_type=CustomIndexType(name='hnsw'),
        parameters={'m': '16', 'ef_construction': '64'},
    )
    _add_index(vector_connection, declared)

    indexdefs = vector_connection.execute(
        f"SELECT indexdef FROM pg_indexes WHERE tablename = '{_TABLE}' AND indexname = %s",  # noqa: S608
        declared.name,
    ).fetchall()
    assert indexdefs == [
        (
            (
                'CREATE INDEX idx_documents_embedding_hnsw ON public.documents '
                "USING hnsw (embedding vector_cosine_ops) WITH (m='16', ef_construction='64')"
            ),
        ),
    ]

    introspected = _introspect_indexes(vector_connection)[declared.name]
    assert introspected.index_type == CustomIndexType(name='hnsw')
    assert introspected.unique is False
    expected_field = IndexField(name='embedding', direction=OrderDirection.ASC, op_class='vector_cosine_ops')
    assert introspected.fields == [expected_field]
    # `TABLE_INDEX_REGISTRY` selects `ic.reloptions`, parsed back into `parameters` -- so a
    # declared index with storage parameters equals its own introspection.
    assert introspected.parameters == {'m': '16', 'ef_construction': '64'}
    assert declared == introspected


def test_ivfflat_index_create_and_introspect(vector_connection: PostgresConnection) -> None:
    declared = IndexSchema(
        name='idx_documents_embedding_ivfflat',
        fields=[IndexField(name='embedding', op_class='vector_cosine_ops')],
        index_type=CustomIndexType(name='ivfflat'),
        parameters={'lists': '10'},
    )
    _add_index(vector_connection, declared)

    indexdefs = vector_connection.execute(
        f"SELECT indexdef FROM pg_indexes WHERE tablename = '{_TABLE}' AND indexname = %s",  # noqa: S608
        declared.name,
    ).fetchall()
    assert indexdefs == [
        (
            (
                'CREATE INDEX idx_documents_embedding_ivfflat ON public.documents '
                "USING ivfflat (embedding vector_cosine_ops) WITH (lists='10')"
            ),
        ),
    ]

    introspected = _introspect_indexes(vector_connection)[declared.name]
    assert introspected.index_type == CustomIndexType(name='ivfflat')
    assert introspected.unique is False
    expected_field = IndexField(name='embedding', direction=OrderDirection.ASC, op_class='vector_cosine_ops')
    assert introspected.fields == [expected_field]
    assert introspected.parameters == {'lists': '10'}
    assert declared == introspected


def test_declared_index_equals_introspected_custom_am_and_op_class(vector_connection: PostgresConnection) -> None:
    # No `parameters` set, so it can't cause the comparison to fail for an unrelated reason.
    declared = IndexSchema(
        name='idx_documents_embedding_hnsw_eq',
        fields=[IndexField(name='embedding', op_class='vector_cosine_ops')],
        index_type=CustomIndexType(name='hnsw'),
    )
    _add_index(vector_connection, declared)

    introspected = _introspect_indexes(vector_connection)[declared.name]
    assert declared == introspected
    assert introspected.index_type == CustomIndexType(name='hnsw')


def test_declared_index_equals_introspected_include_columns(vector_connection: PostgresConnection) -> None:
    declared = IndexSchema(
        name='idx_documents_title_include_body',
        fields=[IndexField(name='title')],
        include=['body'],
    )
    _add_index(vector_connection, declared)

    introspected = _introspect_indexes(vector_connection)[declared.name]
    assert declared == introspected
    assert introspected.include == ['body']


def test_declared_index_equals_introspected_desc_field(vector_connection: PostgresConnection) -> None:
    declared = IndexSchema(
        name='idx_documents_title_desc',
        fields=[IndexField(name='title', direction=OrderDirection.DESC)],
    )
    _add_index(vector_connection, declared)

    introspected = _introspect_indexes(vector_connection)[declared.name]
    assert declared == introspected
    assert introspected.fields[0].direction == OrderDirection.DESC


def test_custom_type_name_case_round_trip(vector_connection: PostgresConnection) -> None:
    """`pg_am.amname` always comes back lowercase; a declaration using mixed case must still equal
    its introspection (`CustomIndexType.__post_init__` casefolds `name` on construction).
    """
    declared = IndexSchema(
        name='idx_documents_embedding_hnsw_case',
        fields=[IndexField(name='embedding', op_class='vector_cosine_ops')],
        index_type=CustomIndexType(name='HNSW'),
    )
    _add_index(vector_connection, declared)

    introspected = _introspect_indexes(vector_connection)[declared.name]
    assert introspected.index_type == CustomIndexType(name='hnsw')
    assert declared == introspected


def test_btree_default_op_class_round_trip(vector_connection: PostgresConnection) -> None:
    """A btree index that explicitly declares the default opclass (`text_ops` for `TEXT`) reads
    back as `op_class=None` (see `TABLE_INDEX_REGISTRY`'s `opc.opcdefault` check) -- `default_op_class`
    lets `IndexSchema.__eq__` resolve the two back to equal instead of comparing unequal forever.
    """
    declared = IndexSchema(
        name='idx_documents_title_text_ops',
        fields=[IndexField(name='title', op_class='text_ops')],
    )
    _add_index(vector_connection, declared)

    introspected = _introspect_indexes(vector_connection)[declared.name]
    assert introspected.fields[0].op_class is None
    assert introspected.fields[0].default_op_class == 'text_ops'
    assert declared == introspected
