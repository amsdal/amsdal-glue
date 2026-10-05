import pytest
from amsdal_glue_core.common.data_models.indexes import CustomIndexType
from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import BuiltinIndexType
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.exceptions import UnsupportedIndexTypeError
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import AddIndex
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection


def _item_schema(*, indexes: list[IndexSchema] | None = None) -> Schema:
    return Schema(
        name='item',
        version=Version.LATEST,
        properties=[PropertySchema(name='embedding', type=ScalarType.TEXT, required=False)],
        indexes=indexes,
    )


def _hnsw() -> IndexSchema:
    return IndexSchema(
        name='idx_item_embedding',
        fields=[IndexField(name='embedding')],
        index_type=CustomIndexType(name='hnsw'),
    )


def _table_names(connection: SqliteConnection) -> list[str]:
    cursor = connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    return [row[0] for row in cursor.fetchall()]


def test_hnsw_register_schema_is_refused_before_ddl(database_connection: SqliteConnection) -> None:
    with pytest.raises(UnsupportedIndexTypeError, match="field 'embedding'") as caught:
        database_connection.run_schema_command(
            SchemaCommand(
                mutations=[
                    RegisterSchema(
                        schema_ref=SchemaReference(name='item', version=Version.LATEST),
                        schema=_item_schema(indexes=[_hnsw()]),
                    ),
                ],
            ),
        )

    message = str(caught.value)
    assert 'hnsw' in message
    assert 'SQLite' in message
    assert 'PostgreSQL' in message
    assert 'item' not in _table_names(database_connection)


def test_later_hnsw_add_index_refuses_the_whole_command(database_connection: SqliteConnection) -> None:
    with pytest.raises(UnsupportedIndexTypeError):
        database_connection.run_schema_command(
            SchemaCommand(
                mutations=[
                    RegisterSchema(
                        schema_ref=SchemaReference(name='item', version=Version.LATEST),
                        schema=_item_schema(),
                    ),
                    AddIndex(
                        schema_ref=SchemaReference(name='item', version=Version.LATEST),
                        index=_hnsw(),
                    ),
                ],
            ),
        )

    assert 'item' not in _table_names(database_connection)


def test_hash_index_is_refused(database_connection: SqliteConnection) -> None:
    with pytest.raises(UnsupportedIndexTypeError, match="'hash'"):
        database_connection.run_schema_command(
            SchemaCommand(
                mutations=[
                    RegisterSchema(
                        schema_ref=SchemaReference(name='item', version=Version.LATEST),
                        schema=_item_schema(
                            indexes=[
                                IndexSchema(
                                    name='idx_item_embedding',
                                    fields=[IndexField(name='embedding')],
                                    index_type=BuiltinIndexType.HASH,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    assert 'item' not in _table_names(database_connection)


def test_btree_index_is_still_created(database_connection: SqliteConnection) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema_ref=SchemaReference(name='item', version=Version.LATEST),
                    schema=_item_schema(
                        indexes=[
                            IndexSchema(
                                name='idx_item_embedding',
                                fields=[IndexField(name='embedding')],
                                index_type=BuiltinIndexType.BTREE,
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )

    assert 'item' in _table_names(database_connection)
