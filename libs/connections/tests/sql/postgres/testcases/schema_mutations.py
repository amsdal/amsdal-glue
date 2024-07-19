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


def create_user_schema(database_connection: PostgresConnection) -> list[Schema | None]:
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

    return database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=schema),
            ],
        ),
    )


def rename_user_schema(database_connection: PostgresConnection) -> list[Schema | None]:
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

    return database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RenameSchema(schema_reference=schema, new_schema_name='customer'),
            ],
        ),
    )


def delete_user_schema(database_connection: PostgresConnection) -> list[Schema | None]:
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

    return database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                DeleteSchema(schema_reference=schema),
            ],
        ),
    )


def add_last_name_property(database_connection: PostgresConnection) -> list[Schema | None]:
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

    return database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                AddProperty(
                    schema_reference=schema,
                    property=PropertySchema(name='last_name', type=str, required=False),
                ),
            ],
        ),
    )


def delete_age_property(database_connection: PostgresConnection) -> list[Schema | None]:
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

    return database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                DeleteProperty(schema_reference=schema, property_name='age'),
            ],
        ),
    )


def update_age_property(database_connection: PostgresConnection) -> list[Schema | None]:
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

    return database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                UpdateProperty(
                    schema_reference=schema,
                    property=PropertySchema(name='age', type=str, required=False),
                ),
            ],
        ),
    )


def add_unique_constraint(database_connection: PostgresConnection) -> list[Schema | None]:
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
    return database_connection.run_schema_command(
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


def delete_unique_constraint(database_connection: PostgresConnection) -> list[Schema | None]:
    return database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                DeleteConstraint(
                    schema_reference=DEFAULT_SCHEMA,
                    constraint_name='uk_user_email_unique',
                ),
            ],
        ),
    )


def add_index(database_connection: PostgresConnection) -> list[Schema | None]:
    return database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                AddIndex(
                    schema_reference=DEFAULT_SCHEMA,
                    index=IndexSchema(name='idx_user_email', fields=['email', 'age'], condition=None),
                ),
            ],
        ),
    )


def delete_index(database_connection: PostgresConnection) -> list[Schema | None]:
    return database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                DeleteIndex(
                    schema_reference=DEFAULT_SCHEMA,
                    index_name='idx_user_email',
                ),
            ],
        ),
    )
