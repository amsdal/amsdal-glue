from unittest.mock import ANY

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import AddConstraint
from amsdal_glue_core.common.operations.mutations.schema import AddIndex
from amsdal_glue_core.common.operations.mutations.schema import AddProperty
from amsdal_glue_core.common.operations.mutations.schema import DeleteConstraint
from amsdal_glue_core.common.operations.mutations.schema import DeleteIndex
from amsdal_glue_core.common.operations.mutations.schema import DeleteProperty
from amsdal_glue_core.common.operations.mutations.schema import DeleteSchema
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import RenameSchema
from amsdal_glue_core.common.operations.mutations.schema import UpdateProperty

DEFAULT_SCHEMA = Schema(
    name='user',
    version=Version.LATEST,
    properties=[
        PropertySchema(
            name='id',
            type=int,
            required=True,
        ),
        PropertySchema(
            name='email',
            type=str,
            required=True,
        ),
        PropertySchema(
            name='age',
            type=int,
            required=True,
        ),
    ],
)


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


def _get_contstraints(database_connection: PostgresConnection, table_name: str) -> list[tuple[str]]:
    return database_connection.execute(
        'SELECT con.conname '  # noqa: S608
        'FROM pg_catalog.pg_constraint con '
        'INNER JOIN pg_catalog.pg_class rel ON rel.oid = con.conrelid '
        'INNER JOIN pg_catalog.pg_namespace nsp ON nsp.oid = connamespace '
        f"WHERE rel.relname = '{table_name}';"
    ).fetchall()


def test_create_schema(database_connection: PostgresConnection) -> None:
    schema = Schema(
        name='user',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='id',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='email',
                type=str,
                required=True,
            ),
            PropertySchema(
                name='age',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='first_name',
                type=str,
                required=False,
            ),
            PropertySchema(
                name='last_name',
                type=str,
                required=False,
            ),
        ],
        constraints=[
            PrimaryKeyConstraint(name='pk_user', fields=['id']),
            UniqueConstraint(name='uk_user_email', fields=['email'], condition=None),
            CheckConstraint(
                name='ck_user_age',
                condition=Conditions(
                    Condition(
                        field=FieldReference(field=Field(name='age'), table_name='user'),
                        lookup=FieldLookup.GT,
                        value=Value(value=18),
                    ),
                ),
            ),
        ],
        indexes=[
            IndexSchema(name='idx_user_email', fields=['first_name', 'last_name']),
        ],
    )

    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=schema),
            ],
        ),
    )

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

    schema = Schema(
        name='user',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='id',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='email',
                type=str,
                required=True,
            ),
            PropertySchema(
                name='age',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='first_name',
                type=str,
                required=False,
            ),
        ],
    )

    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RenameSchema(schema_reference=schema, new_schema_name='customer'),
            ],
        ),
    )

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

    schema = Schema(
        name='user',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='id',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='email',
                type=str,
                required=True,
            ),
            PropertySchema(
                name='age',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='first_name',
                type=str,
                required=False,
            ),
        ],
    )

    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                DeleteSchema(schema_reference=schema),
            ],
        ),
    )

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

    schema = Schema(
        name='user',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='id',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='email',
                type=str,
                required=True,
            ),
            PropertySchema(
                name='age',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='first_name',
                type=str,
                required=False,
            ),
        ],
    )

    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                AddProperty(
                    schema_reference=schema,
                    property=PropertySchema(name='last_name', type=str, required=False),
                ),
            ],
        ),
    )

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

    schema = Schema(
        name='user',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='id',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='email',
                type=str,
                required=True,
            ),
            PropertySchema(
                name='age',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='first_name',
                type=str,
                required=False,
            ),
        ],
    )

    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                DeleteProperty(schema_reference=schema, property_name='age'),
            ],
        ),
    )

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

    schema = Schema(
        name='user',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='id',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='email',
                type=str,
                required=True,
            ),
            PropertySchema(
                name='age',
                type=int,
                required=True,
            ),
        ],
    )

    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                UpdateProperty(
                    schema_reference=schema,
                    property=PropertySchema(name='age', type=str, required=False),
                ),
            ],
        ),
    )

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

    schema = Schema(
        name='user',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='id',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='email',
                type=str,
                required=True,
            ),
            PropertySchema(
                name='age',
                type=int,
                required=True,
            ),
        ],
    )

    assert _get_contstraints(database_connection, 'user') == []

    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                AddConstraint(
                    schema_reference=schema,
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

    assert _get_contstraints(database_connection, 'user') == [('uk_user_email_unique',)]


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
                    schema_reference=DEFAULT_SCHEMA,
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

    assert _get_contstraints(database_connection, 'user') == [('uk_user_email_unique',)]

    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                DeleteConstraint(
                    schema_reference=DEFAULT_SCHEMA,
                    constraint_name='uk_user_email_unique',
                ),
            ],
        ),
    )

    assert _describe_table(database_connection, 'user') == [('id', 'bigint'), ('age', 'bigint'), ('email', 'text')]

    assert _get_contstraints(database_connection, 'user') == []


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

    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                AddIndex(
                    schema_reference=DEFAULT_SCHEMA,
                    index=IndexSchema(name='idx_user_email', fields=['email', 'age'], condition=None),
                ),
            ],
        ),
    )

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
                    schema_reference=DEFAULT_SCHEMA,
                    index=IndexSchema(name='idx_user_email', fields=['email', 'age'], condition=None),
                ),
            ],
        ),
    )

    assert _describe_table(database_connection, 'user') == [('id', 'bigint'), ('age', 'bigint'), ('email', 'text')]

    assert _get_indexes(database_connection, 'user') == [
        ('idx_user_email', 'CREATE INDEX idx_user_email ON public."user" USING btree (email, age)')
    ]

    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                DeleteIndex(
                    schema_reference=DEFAULT_SCHEMA,
                    index_name='idx_user_email',
                ),
            ],
        ),
    )

    assert _get_indexes(database_connection, 'user') == []
