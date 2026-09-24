from amsdal_glue_core.common.data_models.indexes import CustomIndexType
from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.mutations.schema import AddIndex

from ._harness import pg_ddl


def test_add_index_hnsw_with_op_class_and_parameters_pg() -> None:
    m = AddIndex(
        schema_ref=SchemaReference(name='doc', version=Version.LATEST),
        index=IndexSchema(
            name='idx_doc_embedding_hnsw',
            fields=[IndexField(name='embedding', op_class='vector_cosine_ops')],
            index_type=CustomIndexType(name='hnsw'),
            parameters={'m': '16', 'ef_construction': '64'},
        ),
    )
    assert pg_ddl(m) == [
        (
            (
                'CREATE INDEX "idx_doc_embedding_hnsw" ON "doc" USING hnsw ("embedding" vector_cosine_ops) '
                'WITH (m = 16, ef_construction = 64)'
            ),
            [],
        ),
    ]


def test_add_index_ivfflat_with_op_class_and_lists_pg() -> None:
    m = AddIndex(
        schema_ref=SchemaReference(name='doc', version=Version.LATEST),
        index=IndexSchema(
            name='idx_doc_embedding_ivfflat',
            fields=[IndexField(name='embedding', op_class='vector_cosine_ops')],
            index_type=CustomIndexType(name='ivfflat'),
            parameters={'lists': '100'},
        ),
    )
    assert pg_ddl(m) == [
        (
            (
                'CREATE INDEX "idx_doc_embedding_ivfflat" ON "doc" USING ivfflat ("embedding" vector_cosine_ops) '
                'WITH (lists = 100)'
            ),
            [],
        ),
    ]


def test_add_index_custom_access_method_bare_pg() -> None:
    m = AddIndex(
        schema_ref=SchemaReference(name='doc', version=Version.LATEST),
        index=IndexSchema(
            name='idx_doc_embedding_hnsw_bare',
            fields=[IndexField(name='embedding')],
            index_type=CustomIndexType(name='hnsw'),
        ),
    )
    assert pg_ddl(m) == [
        ('CREATE INDEX "idx_doc_embedding_hnsw_bare" ON "doc" USING hnsw ("embedding")', []),
    ]


def test_add_index_custom_access_method_ignores_direction_pg() -> None:
    m = AddIndex(
        schema_ref=SchemaReference(name='doc', version=Version.LATEST),
        index=IndexSchema(
            name='idx_doc_embedding_hnsw_desc',
            fields=[IndexField(name='embedding', direction=OrderDirection.DESC, op_class='vector_cosine_ops')],
            index_type=CustomIndexType(name='hnsw'),
        ),
    )
    sql = pg_ddl(m)[0][0]
    assert sql == 'CREATE INDEX "idx_doc_embedding_hnsw_desc" ON "doc" USING hnsw ("embedding" vector_cosine_ops)'
    assert 'DESC' not in sql
    assert 'ASC' not in sql
