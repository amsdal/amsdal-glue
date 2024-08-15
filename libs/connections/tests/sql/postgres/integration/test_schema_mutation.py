from unittest.mock import ANY

from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import AddConstraint
from amsdal_glue_core.common.operations.mutations.schema import AddIndex
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from tests.sql.postgres.testcases.schema_mutations import add_index
from tests.sql.postgres.testcases.schema_mutations import add_last_name_property
from tests.sql.postgres.testcases.schema_mutations import add_unique_constraint
from tests.sql.postgres.testcases.schema_mutations import create_user_schema
from tests.sql.postgres.testcases.schema_mutations import DEFAULT_SCHEMA
from tests.sql.postgres.testcases.schema_mutations import DEFAULT_SCHEMA_REF
from tests.sql.postgres.testcases.schema_mutations import delete_age_property
from tests.sql.postgres.testcases.schema_mutations import delete_index
from tests.sql.postgres.testcases.schema_mutations import delete_unique_constraint
from tests.sql.postgres.testcases.schema_mutations import delete_user_schema
from tests.sql.postgres.testcases.schema_mutations import rename_user_schema
from tests.sql.postgres.testcases.schema_mutations import update_age_property


def test_create_schema(database_connection: PostgresConnection) -> None:
    create_user_schema(database_connection)

    result = database_connection.execute(
        "SELECT * FROM information_schema.tables WHERE table_name = 'user';"
    ).fetchall()

    assert result == [
        (
            ANY,
            'public',
            'user',
            'BASE TABLE',
            None,
            None,
            None,
            None,
            None,
            'YES',
            'NO',
            None,
        )
    ]

    assert _describe_table(database_connection, 'user') == [
        ('id', 'bigint'),
        ('age', 'bigint'),
        ('email', 'text'),
        ('first_name', 'text'),
        ('last_name', 'text'),
    ]


def test_rename_schema(database_connection: PostgresConnection) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert _describe_table(database_connection, 'user') == [
        ('id', 'bigint'),
        ('age', 'bigint'),
        ('email', 'text'),
    ]

    rename_user_schema(database_connection)

    assert _describe_table(database_connection, 'user') == []

    assert _describe_table(database_connection, 'customer') == [
        ('id', 'bigint'),
        ('age', 'bigint'),
        ('email', 'text'),
    ]


def test_delete_schema(database_connection: PostgresConnection) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert _describe_table(database_connection, 'user') == [('id', 'bigint'), ('age', 'bigint'), ('email', 'text')]

    delete_user_schema(database_connection)

    assert _describe_table(database_connection, 'user') == []


def test_add_property(database_connection: PostgresConnection) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert _describe_table(database_connection, 'user') == [('id', 'bigint'), ('age', 'bigint'), ('email', 'text')]

    add_last_name_property(database_connection)

    assert _describe_table(database_connection, 'user') == [
        ('id', 'bigint'),
        ('age', 'bigint'),
        ('email', 'text'),
        ('last_name', 'text'),
    ]


def test_delete_property(database_connection: PostgresConnection) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert _describe_table(database_connection, 'user') == [('id', 'bigint'), ('age', 'bigint'), ('email', 'text')]

    delete_age_property(database_connection)

    assert _describe_table(database_connection, 'user') == [('id', 'bigint'), ('email', 'text')]


def test_update_property(database_connection: PostgresConnection) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert _describe_table(database_connection, 'user') == [('id', 'bigint'), ('age', 'bigint'), ('email', 'text')]

    update_age_property(database_connection)

    assert _describe_table(database_connection, 'user') == [('id', 'bigint'), ('email', 'text'), ('age', 'text')]


def test_add_constraint(database_connection: PostgresConnection) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert _describe_table(database_connection, 'user') == [('id', 'bigint'), ('age', 'bigint'), ('email', 'text')]
    assert _get_constraints(database_connection, 'user') == []

    add_unique_constraint(database_connection)

    assert _describe_table(database_connection, 'user') == [('id', 'bigint'), ('age', 'bigint'), ('email', 'text')]
    assert _get_constraints(database_connection, 'user') == [('uk_user_email_unique',)]


def test_drop_constraint(database_connection: PostgresConnection) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    database_connection.run_schema_command(
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
    assert _describe_table(database_connection, 'user') == [('id', 'bigint'), ('age', 'bigint'), ('email', 'text')]
    assert _get_constraints(database_connection, 'user') == [('uk_user_email_unique',)]

    delete_unique_constraint(database_connection)

    assert _describe_table(database_connection, 'user') == [('id', 'bigint'), ('age', 'bigint'), ('email', 'text')]
    assert _get_constraints(database_connection, 'user') == []


def test_add_index(database_connection: PostgresConnection) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=DEFAULT_SCHEMA),
            ],
        ),
    )
    assert _describe_table(database_connection, 'user') == [('id', 'bigint'), ('age', 'bigint'), ('email', 'text')]
    assert _get_indexes(database_connection, 'user') == []

    add_index(database_connection)

    assert _describe_table(database_connection, 'user') == [('id', 'bigint'), ('age', 'bigint'), ('email', 'text')]
    assert _get_indexes(database_connection, 'user') == [
        ('idx_user_email', 'CREATE INDEX idx_user_email ON public."user" USING btree (email, age)')
    ]


def test_delete_index(database_connection: PostgresConnection) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                AddIndex(
                    schema_reference=DEFAULT_SCHEMA_REF,
                    index=IndexSchema(name='idx_user_email', fields=['email', 'age'], condition=None),
                ),
            ],
        ),
    )

    assert _describe_table(database_connection, 'user') == [('id', 'bigint'), ('age', 'bigint'), ('email', 'text')]
    assert _get_indexes(database_connection, 'user') == [
        ('idx_user_email', 'CREATE INDEX idx_user_email ON public."user" USING btree (email, age)')
    ]

    delete_index(database_connection)

    assert _get_indexes(database_connection, 'user') == []


def _get_indexes(database_connection: PostgresConnection, table_name: str) -> list[tuple[str, str]]:
    return database_connection.execute(
        f"SELECT indexname, indexdef FROM pg_indexes WHERE tablename = '{table_name}'"  # noqa: S608
    ).fetchall()


def _describe_table(database_connection: PostgresConnection, table_name: str) -> list[tuple[str, str]]:
    return database_connection.execute(
        'SELECT column_name, data_type '  # noqa: S608
        'FROM information_schema.columns '
        f"WHERE table_name = '{table_name}';"
    ).fetchall()


def _get_constraints(database_connection: PostgresConnection, table_name: str) -> list[tuple[str]]:
    return database_connection.execute(
        'SELECT con.conname '  # noqa: S608
        'FROM pg_catalog.pg_constraint con '
        'INNER JOIN pg_catalog.pg_class rel ON rel.oid = con.conrelid '
        'INNER JOIN pg_catalog.pg_namespace nsp ON nsp.oid = connamespace '
        f"WHERE rel.relname = '{table_name}';"
    ).fetchall()
