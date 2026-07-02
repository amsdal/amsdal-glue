import pytest
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.indexes import IndexSchema
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
async def test_create_schema(database_connection: AsyncPostgresConnection) -> None:
    await create_user_schema(database_connection)

    assert await _describe_table(database_connection, 'user') == [
        ('id', 'bigint'),
        ('age', 'bigint'),
        ('email', 'text'),
        ('first_name', 'text'),
        ('last_name', 'text'),
    ]


@pytest.mark.asyncio
async def test_rename_schema(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema_ref=DEFAULT_SCHEMA_REF, schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert await _describe_table(database_connection, 'user') == [
        ('id', 'bigint'),
        ('age', 'bigint'),
        ('email', 'text'),
    ]

    await rename_user_schema(database_connection)

    assert await _describe_table(database_connection, 'user') == []

    assert await _describe_table(database_connection, 'customer') == [
        ('id', 'bigint'),
        ('age', 'bigint'),
        ('email', 'text'),
    ]


@pytest.mark.asyncio
async def test_delete_schema(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema_ref=DEFAULT_SCHEMA_REF, schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert await _describe_table(database_connection, 'user') == [
        ('id', 'bigint'),
        ('age', 'bigint'),
        ('email', 'text'),
    ]

    await delete_user_schema(database_connection)

    assert await _describe_table(database_connection, 'user') == []


@pytest.mark.asyncio
async def test_add_property(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema_ref=DEFAULT_SCHEMA_REF, schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert await _describe_table(database_connection, 'user') == [
        ('id', 'bigint'),
        ('age', 'bigint'),
        ('email', 'text'),
    ]

    await add_last_name_property(database_connection)

    assert await _describe_table(database_connection, 'user') == [
        ('id', 'bigint'),
        ('age', 'bigint'),
        ('email', 'text'),
        ('last_name', 'text'),
    ]


@pytest.mark.asyncio
async def test_delete_property(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema_ref=DEFAULT_SCHEMA_REF, schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert await _describe_table(database_connection, 'user') == [
        ('id', 'bigint'),
        ('age', 'bigint'),
        ('email', 'text'),
    ]

    await delete_age_property(database_connection)

    assert await _describe_table(database_connection, 'user') == [('id', 'bigint'), ('email', 'text')]


@pytest.mark.asyncio
async def test_update_property(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema_ref=DEFAULT_SCHEMA_REF, schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert await _describe_table(database_connection, 'user') == [
        ('id', 'bigint'),
        ('age', 'bigint'),
        ('email', 'text'),
    ]

    await update_age_property(database_connection)

    assert await _describe_table(database_connection, 'user') == [
        ('id', 'bigint'),
        ('email', 'text'),
        ('age', 'text'),
    ]


@pytest.mark.asyncio
@pytest.mark.skip(reason='Skipping constraint tests due to intermittent failures.')
async def test_add_constraint(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema_ref=DEFAULT_SCHEMA_REF, schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert await _describe_table(database_connection, 'user') == [
        ('id', 'bigint'),
        ('age', 'bigint'),
        ('email', 'text'),
    ]
    assert await _get_constraints(database_connection, 'user') == []

    await add_unique_constraint(database_connection)

    assert await _describe_table(database_connection, 'user') == [
        ('id', 'bigint'),
        ('age', 'bigint'),
        ('email', 'text'),
    ]
    assert await _get_constraints(database_connection, 'user') == [('uk_user_email_unique',)]


@pytest.mark.asyncio
@pytest.mark.skip(reason='Skipping constraint tests due to intermittent failures.')
async def test_drop_constraint(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema_ref=DEFAULT_SCHEMA_REF, schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    await database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                AddConstraint(
                    schema_ref=DEFAULT_SCHEMA_REF,
                    constraint=UniqueConstraint(
                        name='uk_user_email_unique',
                        fields=['email', 'age'],
                        condition=None,
                    ),
                ),
            ],
        ),
    )
    assert await _describe_table(database_connection, 'user') == [
        ('id', 'bigint'),
        ('age', 'bigint'),
        ('email', 'text'),
    ]
    assert await _get_constraints(database_connection, 'user') == [('uk_user_email_unique',)]

    await delete_unique_constraint(database_connection)

    assert await _describe_table(database_connection, 'user') == [
        ('id', 'bigint'),
        ('age', 'bigint'),
        ('email', 'text'),
    ]
    assert await _get_constraints(database_connection, 'user') == []


@pytest.mark.asyncio
async def test_add_index(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema_ref=DEFAULT_SCHEMA_REF, schema=DEFAULT_SCHEMA),
            ],
        ),
    )
    assert await _describe_table(database_connection, 'user') == [
        ('id', 'bigint'),
        ('age', 'bigint'),
        ('email', 'text'),
    ]
    assert await _get_indexes(database_connection, 'user') == []

    await add_index(database_connection)

    assert await _describe_table(database_connection, 'user') == [
        ('id', 'bigint'),
        ('age', 'bigint'),
        ('email', 'text'),
    ]
    assert await _get_indexes(database_connection, 'user') == [
        ('idx_user_email', 'CREATE INDEX idx_user_email ON public."user" USING btree (email, age)')
    ]


@pytest.mark.asyncio
async def test_delete_index(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema_ref=DEFAULT_SCHEMA_REF, schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    await database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                AddIndex(
                    schema_ref=DEFAULT_SCHEMA_REF,
                    index=IndexSchema(
                        name='idx_user_email',
                        fields=[IndexField(name='email'), IndexField(name='age')],
                        condition=None,
                    ),
                ),
            ],
        ),
    )

    assert await _describe_table(database_connection, 'user') == [
        ('id', 'bigint'),
        ('age', 'bigint'),
        ('email', 'text'),
    ]
    assert await _get_indexes(database_connection, 'user') == [
        ('idx_user_email', 'CREATE INDEX idx_user_email ON public."user" USING btree (email, age)')
    ]

    await delete_index(database_connection)

    assert await _get_indexes(database_connection, 'user') == []


async def _get_indexes(database_connection: AsyncPostgresConnection, table_name: str) -> list[tuple[str, str]]:
    cursor = await database_connection.execute(
        f"SELECT indexname, indexdef FROM pg_indexes WHERE tablename = '{table_name}'"  # noqa: S608
    )
    return await cursor.fetchall()


async def _describe_table(database_connection: AsyncPostgresConnection, table_name: str) -> list[tuple[str, str]]:
    cursor = await database_connection.execute(
        'SELECT column_name, data_type '  # noqa: S608
        'FROM information_schema.columns '
        f"WHERE table_name = '{table_name}';"
    )
    return await cursor.fetchall()


async def _get_constraints(database_connection: AsyncPostgresConnection, table_name: str) -> list[tuple[str]]:
    cursor = await database_connection.execute(
        'SELECT con.conname '  # noqa: S608
        'FROM pg_catalog.pg_constraint con '
        'INNER JOIN pg_catalog.pg_class rel ON rel.oid = con.conrelid '
        'INNER JOIN pg_catalog.pg_namespace nsp ON nsp.oid = connamespace '
        f"WHERE rel.relname = '{table_name}';"
    )
    return await cursor.fetchall()
