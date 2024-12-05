from collections.abc import AsyncGenerator
from typing import Union

import pytest
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import FIELD_TYPE
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import AddConstraint
from amsdal_glue_core.common.operations.mutations.schema import AddIndex
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.postgres_connection import AsyncPostgresConnection
from tests.sql.aio_postgres.testcases.schema_mutations import add_index
from tests.sql.aio_postgres.testcases.schema_mutations import add_last_name_property
from tests.sql.aio_postgres.testcases.schema_mutations import add_unique_constraint
from tests.sql.aio_postgres.testcases.schema_mutations import create_user_schema
from tests.sql.aio_postgres.testcases.schema_mutations import DEFAULT_SCHEMA
from tests.sql.aio_postgres.testcases.schema_mutations import DEFAULT_SCHEMA_REF
from tests.sql.aio_postgres.testcases.schema_mutations import delete_age_property
from tests.sql.aio_postgres.testcases.schema_mutations import delete_index
from tests.sql.aio_postgres.testcases.schema_mutations import delete_unique_constraint
from tests.sql.aio_postgres.testcases.schema_mutations import delete_user_schema
from tests.sql.aio_postgres.testcases.schema_mutations import rename_user_schema
from tests.sql.aio_postgres.testcases.schema_mutations import update_age_property


@pytest.mark.asyncio
async def test_create_schema(database_connection: AsyncGenerator[AsyncPostgresConnection, None]) -> None:
    async for dc in database_connection:
        await create_user_schema(dc)

        assert await _describe_table(dc, 'user') == [
            ('id', int),
            ('age', int),
            ('email', str),
            ('first_name', str),
            ('last_name', str),
        ]


@pytest.mark.asyncio
async def test_rename_schema(database_connection: AsyncGenerator[AsyncPostgresConnection, None]) -> None:
    async for dc in database_connection:
        await dc.run_schema_command(
            SchemaCommand(
                mutations=[
                    RegisterSchema(schema=DEFAULT_SCHEMA),
                ],
            ),
        )

        assert await _describe_table(dc, 'user') == [
            ('id', int),
            ('age', int),
            ('email', str),
        ]

        await rename_user_schema(dc)

        assert await _describe_table(dc, 'user') == []

        assert await _describe_table(dc, 'customer') == [
            ('id', int),
            ('age', int),
            ('email', str),
        ]


@pytest.mark.asyncio
async def test_delete_schema(database_connection: AsyncGenerator[AsyncPostgresConnection, None]) -> None:
    async for dc in database_connection:
        await dc.run_schema_command(
            SchemaCommand(
                mutations=[
                    RegisterSchema(schema=DEFAULT_SCHEMA),
                ],
            ),
        )

        assert await _describe_table(dc, 'user') == [('id', int), ('age', int), ('email', str)]

        await delete_user_schema(dc)

        assert await _describe_table(dc, 'user') == []


@pytest.mark.asyncio
async def test_add_property(database_connection: AsyncGenerator[AsyncPostgresConnection, None]) -> None:
    async for dc in database_connection:
        await dc.run_schema_command(
            SchemaCommand(
                mutations=[
                    RegisterSchema(schema=DEFAULT_SCHEMA),
                ],
            ),
        )

        assert await _describe_table(dc, 'user') == [('id', int), ('age', int), ('email', str)]

        await add_last_name_property(dc)

        assert await _describe_table(dc, 'user') == [
            ('id', int),
            ('age', int),
            ('email', str),
            ('last_name', str),
        ]


@pytest.mark.asyncio
async def test_delete_property(database_connection: AsyncGenerator[AsyncPostgresConnection, None]) -> None:
    async for dc in database_connection:
        await dc.run_schema_command(
            SchemaCommand(
                mutations=[
                    RegisterSchema(schema=DEFAULT_SCHEMA),
                ],
            ),
        )

        assert await _describe_table(dc, 'user') == [('id', int), ('age', int), ('email', str)]

        await delete_age_property(dc)

        assert await _describe_table(dc, 'user') == [('id', int), ('email', str)]


@pytest.mark.asyncio
async def test_update_property(database_connection: AsyncGenerator[AsyncPostgresConnection, None]) -> None:
    async for dc in database_connection:
        await dc.run_schema_command(
            SchemaCommand(
                mutations=[
                    RegisterSchema(schema=DEFAULT_SCHEMA),
                ],
            ),
        )

        assert await _describe_table(dc, 'user') == [('id', int), ('age', int), ('email', str)]

        await update_age_property(dc)

        assert await _describe_table(dc, 'user') == [('id', int), ('email', str), ('age', str)]


@pytest.mark.asyncio
async def test_add_constraint(database_connection: AsyncGenerator[AsyncPostgresConnection, None]) -> None:
    async for dc in database_connection:
        await dc.run_schema_command(
            SchemaCommand(
                mutations=[
                    RegisterSchema(schema=DEFAULT_SCHEMA),
                ],
            ),
        )

        assert await _describe_table(dc, 'user') == [('id', int), ('age', int), ('email', str)]
        assert await _get_constraints(dc, 'user') == []

        await add_unique_constraint(dc)

        assert await _describe_table(dc, 'user') == [('id', int), ('age', int), ('email', str)]
        assert await _get_constraints(dc, 'user') == [('uk_user_email_unique',)]


@pytest.mark.asyncio
async def test_drop_constraint(database_connection: AsyncGenerator[AsyncPostgresConnection, None]) -> None:
    async for dc in database_connection:
        await dc.run_schema_command(
            SchemaCommand(
                mutations=[
                    RegisterSchema(schema=DEFAULT_SCHEMA),
                ],
            ),
        )

        await dc.run_schema_command(
            SchemaCommand(
                mutations=[
                    AddConstraint(
                        schema_reference=DEFAULT_SCHEMA_REF,
                        constraint=UniqueConstraint(
                            name='uk_user_email_unique',
                            fields=['email', 'age'],
                            condition=None,
                        ),
                    ),
                ],
            ),
        )
        assert await _describe_table(dc, 'user') == [('id', int), ('age', int), ('email', str)]
        assert await _get_constraints(dc, 'user') == [('uk_user_email_unique',)]

        await delete_unique_constraint(dc)

        assert await _describe_table(dc, 'user') == [('id', int), ('age', int), ('email', str)]
        assert await _get_constraints(dc, 'user') == []


@pytest.mark.asyncio
async def test_add_index(database_connection: AsyncGenerator[AsyncPostgresConnection, None]) -> None:
    async for dc in database_connection:
        await dc.run_schema_command(
            SchemaCommand(
                mutations=[
                    RegisterSchema(schema=DEFAULT_SCHEMA),
                ],
            ),
        )
        assert await _describe_table(dc, 'user') == [('id', int), ('age', int), ('email', str)]
        assert await _get_indexes(dc, 'user') == []

        await add_index(dc)

        assert await _describe_table(dc, 'user') == [('id', int), ('age', int), ('email', str)]
        assert await _get_indexes(dc, 'user') == [
            ('idx_user_email', ['email', 'age']),
        ]


@pytest.mark.asyncio
async def test_delete_index(database_connection: AsyncGenerator[AsyncPostgresConnection, None]) -> None:
    async for dc in database_connection:
        await dc.run_schema_command(
            SchemaCommand(
                mutations=[
                    RegisterSchema(schema=DEFAULT_SCHEMA),
                ],
            ),
        )

        await dc.run_schema_command(
            SchemaCommand(
                mutations=[
                    AddIndex(
                        schema_reference=DEFAULT_SCHEMA_REF,
                        index=IndexSchema(name='idx_user_email', fields=['email', 'age'], condition=None),
                    ),
                ],
            ),
        )

        assert await _describe_table(dc, 'user') == [('id', int), ('age', int), ('email', str)]
        assert await _get_indexes(dc, 'user') == [
            ('idx_user_email', ['email', 'age']),
        ]

        await delete_index(dc)

        assert await _get_indexes(dc, 'user') == []


async def _get_indexes(database_connection: AsyncPostgresConnection, table_name: str) -> list[tuple[str, list[str]]]:
    _, _, indexes = await database_connection.get_table_info(table_name)

    return [(index.name, index.fields) for index in indexes]


async def _describe_table(
    database_connection: AsyncPostgresConnection, table_name: str
) -> list[tuple[str, Union[Schema, 'SchemaReference', FIELD_TYPE]]]:
    properties, _, _ = await database_connection.get_table_info(table_name)

    return [(prop.name, prop.type) for prop in properties]


async def _get_constraints(database_connection: AsyncPostgresConnection, table_name: str) -> list[tuple[str]]:
    _, constraints, _ = await database_connection.get_table_info(table_name)

    return [(constraint.name,) for constraint in constraints]
