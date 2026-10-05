import sys
import types
from typing import Any

import pytest
from amsdal_glue_core.common.data_models.indexes import CustomIndexType
from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.exceptions import UnsupportedIndexTypeError
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema


def _elasticsearch_connection() -> Any:
    try:
        from amsdal_glue_connections.elasticsearch_connection.sync_connection import ElasticsearchConnection
    except ModuleNotFoundError:
        stub = types.ModuleType('elasticsearch')

        class Elasticsearch:
            pass

        class NotFoundError(Exception):
            pass

        stub.Elasticsearch = Elasticsearch  # type: ignore[attr-defined]
        stub.NotFoundError = NotFoundError  # type: ignore[attr-defined]
        sys.modules['elasticsearch'] = stub
        from amsdal_glue_connections.elasticsearch_connection.sync_connection import ElasticsearchConnection

    return ElasticsearchConnection


class _Indices:
    def create(self, **_kwargs: object) -> None:
        msg = 'DDL ran'
        raise AssertionError(msg)

    def get(self, **_kwargs: object) -> None:
        msg = 'DDL ran'
        raise AssertionError(msg)

    def put_mapping(self, **_kwargs: object) -> None:
        msg = 'DDL ran'
        raise AssertionError(msg)


class _Stub:
    indices = _Indices()


def test_hnsw_is_refused_before_elasticsearch_ddl() -> None:
    connection_cls = _elasticsearch_connection()
    connection = connection_cls()
    connection._connection = _Stub()  # type: ignore[assignment]  # noqa: SLF001

    with pytest.raises(UnsupportedIndexTypeError, match="field 'embedding'") as caught:
        connection.run_schema_command(
            SchemaCommand(
                mutations=[
                    RegisterSchema(
                        schema_ref=SchemaReference(name='item', version=Version.LATEST),
                        schema=Schema(
                            name='item',
                            version=Version.LATEST,
                            properties=[PropertySchema(name='embedding', type=ScalarType.TEXT, required=False)],
                            indexes=[
                                IndexSchema(
                                    name='idx_item_embedding',
                                    fields=[IndexField(name='embedding')],
                                    index_type=CustomIndexType(name='hnsw'),
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    message = str(caught.value)
    assert 'hnsw' in message
    assert 'Elasticsearch' in message
    assert 'PostgreSQL' in message
