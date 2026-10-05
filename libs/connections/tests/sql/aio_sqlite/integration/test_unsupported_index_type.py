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

from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection


async def test_hnsw_register_schema_is_refused_before_ddl(database_connection: AsyncSqliteConnection) -> None:
    with pytest.raises(UnsupportedIndexTypeError, match="field 'embedding'") as caught:
        await database_connection.run_schema_command(
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
    assert 'SQLite' in message
    assert 'PostgreSQL' in message
    cursor = await database_connection.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'item'")
    assert await cursor.fetchall() == []
