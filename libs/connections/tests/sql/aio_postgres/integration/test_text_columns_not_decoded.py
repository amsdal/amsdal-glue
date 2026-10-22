"""A string column's value is text, whatever it looks like; only non-text values that look like JSON are decoded.

Before: any string starting with `{`/`[` and ending with `}`/`]` was `json.loads`-ed, so a stored source-code
chunk such as `{ x: 1 }` failed the whole query and one that happened to be valid JSON came back as a dict.
"""

import pytest
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression

from amsdal_glue_connections.sql.connections.postgres_connection import AsyncPostgresConnection

ROWS = [
    (1, '{ x: 1 }', '{\n  foo: bar\n}'),
    (2, '[1, 2]', '{"a": 1}'),
    (3, 'plain', '[not json'),
]


async def _query(connection: AsyncPostgresConnection) -> list[dict]:
    rows = await connection.query(
        QueryStatement(
            table=SchemaReference(name='chunks', alias='c', version=Version.LATEST),
            order_by=[
                OrderByQuery(
                    expression=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='id'), table_name='c')
                    ),
                    direction=OrderDirection.ASC,
                )
            ],
        )
    )
    return [r.data for r in rows]


@pytest.mark.asyncio
async def test_text_and_varchar_values_come_back_as_stored(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.execute('CREATE TABLE chunks (id INT PRIMARY KEY, body TEXT, label VARCHAR(64))')
    for row in ROWS:
        await database_connection.execute('INSERT INTO chunks (id, body, label) VALUES (%s, %s, %s)', *row)

    assert await _query(database_connection) == [{'id': i, 'body': b, 'label': lb} for i, b, lb in ROWS]


@pytest.mark.asyncio
async def test_jsonb_and_vector_values_are_still_decoded(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.execute('CREATE EXTENSION IF NOT EXISTS vector')
    await database_connection.execute('CREATE TABLE chunks (id INT PRIMARY KEY, meta JSONB, embedding vector(3))')
    await database_connection.execute(
        'INSERT INTO chunks (id, meta, embedding) VALUES (%s, %s::jsonb, %s::vector)', 1, '{"a": [1, 2]}', '[1,2,3]'
    )

    assert await _query(database_connection) == [{'id': 1, 'meta': {'a': [1, 2]}, 'embedding': [1.0, 2.0, 3.0]}]
