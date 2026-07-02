import pytest
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import AddConstraint
from amsdal_glue_core.common.operations.mutations.schema import AddIndex
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection
from tests.sql.aio_sqlite.testcases.schema_mutations import add_index
from tests.sql.aio_sqlite.testcases.schema_mutations import add_last_name_property
from tests.sql.aio_sqlite.testcases.schema_mutations import add_unique_constraint
from tests.sql.aio_sqlite.testcases.schema_mutations import create_user_schema
from tests.sql.aio_sqlite.testcases.schema_mutations import DEFAULT_SCHEMA
from tests.sql.aio_sqlite.testcases.schema_mutations import DEFAULT_SCHEMA_REF
from tests.sql.aio_sqlite.testcases.schema_mutations import delete_age_property
from tests.sql.aio_sqlite.testcases.schema_mutations import delete_index
from tests.sql.aio_sqlite.testcases.schema_mutations import delete_unique_constraint
from tests.sql.aio_sqlite.testcases.schema_mutations import delete_user_schema
from tests.sql.aio_sqlite.testcases.schema_mutations import rename_user_schema
from tests.sql.aio_sqlite.testcases.schema_mutations import update_age_property


@pytest.mark.asyncio
async def test_create_schema(database_connection: AsyncSqliteConnection) -> None:
    await create_user_schema(database_connection)

    assert await _describe_table(database_connection, 'user') == [
        ('id', ScalarType.INTEGER),
        ('email', ScalarType.TEXT),
        ('age', ScalarType.INTEGER),
        ('first_name', ScalarType.TEXT),
        ('last_name', ScalarType.TEXT),
    ]


@pytest.mark.asyncio
async def test_rename_schema(database_connection: AsyncSqliteConnection) -> None:
    await database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema_ref=DEFAULT_SCHEMA_REF, schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert await _describe_table(database_connection, 'user') == [
        ('id', ScalarType.INTEGER),
        ('email', ScalarType.TEXT),
        ('age', ScalarType.INTEGER),
    ]

    await rename_user_schema(database_connection)

    assert await _describe_table(database_connection, 'user') == []

    assert await _describe_table(database_connection, 'customer') == [
        ('id', ScalarType.INTEGER),
        ('email', ScalarType.TEXT),
        ('age', ScalarType.INTEGER),
    ]


@pytest.mark.asyncio
async def test_delete_schema(database_connection: AsyncSqliteConnection) -> None:
    await database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema_ref=DEFAULT_SCHEMA_REF, schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert await _describe_table(database_connection, 'user') == [
        ('id', ScalarType.INTEGER),
        ('email', ScalarType.TEXT),
        ('age', ScalarType.INTEGER),
    ]

    await delete_user_schema(database_connection)

    assert await _describe_table(database_connection, 'user') == []


@pytest.mark.asyncio
async def test_add_property(database_connection: AsyncSqliteConnection) -> None:
    await database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema_ref=DEFAULT_SCHEMA_REF, schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert await _describe_table(database_connection, 'user') == [
        ('id', ScalarType.INTEGER),
        ('email', ScalarType.TEXT),
        ('age', ScalarType.INTEGER),
    ]

    await add_last_name_property(database_connection)

    assert await _describe_table(database_connection, 'user') == [
        ('id', ScalarType.INTEGER),
        ('email', ScalarType.TEXT),
        ('age', ScalarType.INTEGER),
        ('last_name', ScalarType.TEXT),
    ]


@pytest.mark.asyncio
async def test_delete_property(database_connection: AsyncSqliteConnection) -> None:
    await database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema_ref=DEFAULT_SCHEMA_REF, schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert await _describe_table(database_connection, 'user') == [
        ('id', ScalarType.INTEGER),
        ('email', ScalarType.TEXT),
        ('age', ScalarType.INTEGER),
    ]

    await delete_age_property(database_connection)

    assert await _describe_table(database_connection, 'user') == [
        ('id', ScalarType.INTEGER),
        ('email', ScalarType.TEXT),
    ]


@pytest.mark.asyncio
async def test_update_property(database_connection: AsyncSqliteConnection) -> None:
    await database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema_ref=DEFAULT_SCHEMA_REF, schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert await _describe_table(database_connection, 'user') == [
        ('id', ScalarType.INTEGER),
        ('email', ScalarType.TEXT),
        ('age', ScalarType.INTEGER),
    ]

    await update_age_property(database_connection)

    assert await _describe_table(database_connection, 'user') == [
        ('id', ScalarType.INTEGER),
        ('email', ScalarType.TEXT),
        ('age', ScalarType.TEXT),
    ]


@pytest.mark.asyncio
async def test_add_constraint(database_connection: AsyncSqliteConnection) -> None:
    await database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema_ref=DEFAULT_SCHEMA_REF, schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert await _describe_table(database_connection, 'user') == [
        ('id', ScalarType.INTEGER),
        ('email', ScalarType.TEXT),
        ('age', ScalarType.INTEGER),
    ]
    assert await _get_constraints(database_connection, 'user') == []

    await add_unique_constraint(database_connection)

    assert await _describe_table(database_connection, 'user') == [
        ('id', ScalarType.INTEGER),
        ('email', ScalarType.TEXT),
        ('age', ScalarType.INTEGER),
    ]
    assert await _get_constraints(database_connection, 'user') == [('uk_user_email_unique',)]


@pytest.mark.asyncio
async def test_drop_constraint(database_connection: AsyncSqliteConnection) -> None:
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
        ('id', ScalarType.INTEGER),
        ('email', ScalarType.TEXT),
        ('age', ScalarType.INTEGER),
    ]
    assert await _get_constraints(database_connection, 'user') == [('uk_user_email_unique',)]

    await delete_unique_constraint(database_connection)

    assert await _describe_table(database_connection, 'user') == [
        ('id', ScalarType.INTEGER),
        ('email', ScalarType.TEXT),
        ('age', ScalarType.INTEGER),
    ]
    assert await _get_constraints(database_connection, 'user') == []


@pytest.mark.asyncio
async def test_add_index(database_connection: AsyncSqliteConnection) -> None:
    await database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema_ref=DEFAULT_SCHEMA_REF, schema=DEFAULT_SCHEMA),
            ],
        ),
    )
    assert await _describe_table(database_connection, 'user') == [
        ('id', ScalarType.INTEGER),
        ('email', ScalarType.TEXT),
        ('age', ScalarType.INTEGER),
    ]
    assert await _get_indexes(database_connection, 'user') == []

    await add_index(database_connection)

    assert await _describe_table(database_connection, 'user') == [
        ('id', ScalarType.INTEGER),
        ('email', ScalarType.TEXT),
        ('age', ScalarType.INTEGER),
    ]
    assert await _get_indexes(database_connection, 'user') == [
        ('idx_user_email', ['email', 'age']),
    ]


@pytest.mark.asyncio
async def test_delete_index(database_connection: AsyncSqliteConnection) -> None:
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
        ('id', ScalarType.INTEGER),
        ('email', ScalarType.TEXT),
        ('age', ScalarType.INTEGER),
    ]
    assert await _get_indexes(database_connection, 'user') == [
        ('idx_user_email', ['email', 'age']),
    ]

    await delete_index(database_connection)

    assert await _get_indexes(database_connection, 'user') == []


async def _get_indexes(database_connection: AsyncSqliteConnection, table_name: str) -> list[tuple[str, list[str]]]:
    _, _, indexes = await database_connection.get_table_info(table_name)

    return [(index.name, [f.name for f in index.fields]) for index in indexes]


async def _describe_table(database_connection: AsyncSqliteConnection, table_name: str) -> list[tuple]:
    properties, _, _ = await database_connection.get_table_info(table_name)

    return [(prop.name, prop.type) for prop in properties]


async def _get_constraints(database_connection: AsyncSqliteConnection, table_name: str) -> list[tuple[str]]:
    _, constraints, _ = await database_connection.get_table_info(table_name)

    return [(constraint.name,) for constraint in constraints]
