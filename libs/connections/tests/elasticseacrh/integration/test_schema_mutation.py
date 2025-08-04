from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import AddConstraint
from amsdal_glue_core.common.operations.mutations.schema import AddIndex
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.elasticsearch_connection.sync_connection import ElasticsearchConnection

from ..testcases.schema_mutations import add_index
from ..testcases.schema_mutations import add_last_name_property
from ..testcases.schema_mutations import add_unique_constraint
from ..testcases.schema_mutations import create_user_schema
from ..testcases.schema_mutations import DEFAULT_SCHEMA
from ..testcases.schema_mutations import DEFAULT_SCHEMA_REF
from ..testcases.schema_mutations import delete_age_property
from ..testcases.schema_mutations import delete_index
from ..testcases.schema_mutations import delete_unique_constraint
from ..testcases.schema_mutations import delete_user_schema
from ..testcases.schema_mutations import rename_user_schema
from ..testcases.schema_mutations import update_age_property


def test_create_schema(database_connection: ElasticsearchConnection, test_prefix: str) -> None:
    create_user_schema(database_connection)

    result = database_connection.query_schema()

    # Check that one schema was created
    assert len(result) == 1
    schema = result[0]

    # Verify schema name (includes prefix and version suffix)
    assert schema.name == f'{test_prefix}user'

    # Verify properties (order may vary in Elasticsearch)
    expected_properties = [
        PropertySchema(name='age', type=int, required=False),
        PropertySchema(name='email', type=str, required=False),
        PropertySchema(name='first_name', type=str, required=False),
        PropertySchema(name='id', type=int, required=False),
        PropertySchema(name='last_name', type=str, required=False),
    ]

    # Sort both property lists by name for comparison
    actual_properties_sorted = sorted(schema.properties, key=lambda p: p.name)
    expected_properties_sorted = sorted(expected_properties, key=lambda p: p.name)
    assert actual_properties_sorted == expected_properties_sorted

    # Verify constraints were preserved
    assert schema.constraints is not None
    assert len(schema.constraints) == 3
    constraint_names = {c.name for c in schema.constraints}
    assert constraint_names == {'ck_user_age', 'uk_user_email', 'pk_user'}

    # Verify indexes were preserved
    assert schema.indexes is not None
    assert len(schema.indexes) == 1
    assert schema.indexes[0].name == 'idx_user_email'
    assert schema.indexes[0].fields == ['first_name', 'last_name']


def test_rename_schema(database_connection: ElasticsearchConnection, test_prefix: str) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    result = database_connection.query_schema()
    assert result == [
        Schema(
            name=f'{test_prefix}user',
            properties=[
                PropertySchema(name='age', type=int, required=False),
                PropertySchema(name='email', type=str, required=False),
                PropertySchema(name='id', type=int, required=False),
            ],
            indexes=[],
            constraints=[],
        )
    ]

    rename_user_schema(database_connection)

    result = database_connection.query_schema()
    assert result == [
        Schema(
            name=f'{test_prefix}customer',
            properties=[
                PropertySchema(name='age', type=int, required=False),
                PropertySchema(name='email', type=str, required=False),
                PropertySchema(name='id', type=int, required=False),
            ],
            indexes=[],
            constraints=[],
        )
    ]


def test_delete_schema(database_connection: ElasticsearchConnection, test_prefix: str) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    result = database_connection.query_schema()
    assert result == [
        Schema(
            name=f'{test_prefix}user',
            properties=[
                PropertySchema(name='age', type=int, required=False),
                PropertySchema(name='email', type=str, required=False),
                PropertySchema(name='id', type=int, required=False),
            ],
            indexes=[],
            constraints=[],
        )
    ]
    delete_user_schema(database_connection)

    result = database_connection.query_schema()

    assert result == []


def test_add_property(database_connection: ElasticsearchConnection, test_prefix: str) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    result = database_connection.query_schema()
    assert result == [
        Schema(
            name=f'{test_prefix}user',
            properties=[
                PropertySchema(name='age', type=int, required=False),
                PropertySchema(name='email', type=str, required=False),
                PropertySchema(name='id', type=int, required=False),
            ],
            indexes=[],
            constraints=[],
        )
    ]

    add_last_name_property(database_connection)

    result = database_connection.query_schema()
    assert result == [
        Schema(
            name=f'{test_prefix}user',
            properties=[
                PropertySchema(name='age', type=int, required=False),
                PropertySchema(name='email', type=str, required=False),
                PropertySchema(name='id', type=int, required=False),
                PropertySchema(name='last_name', type=str, required=False),
            ],
            indexes=[],
            constraints=[],
        )
    ]


def test_delete_property(database_connection: ElasticsearchConnection, test_prefix: str) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    result = database_connection.query_schema()
    assert result == [
        Schema(
            name=f'{test_prefix}user',
            properties=[
                PropertySchema(name='age', type=int, required=False),
                PropertySchema(name='email', type=str, required=False),
                PropertySchema(name='id', type=int, required=False),
            ],
            indexes=[],
            constraints=[],
        )
    ]

    delete_age_property(database_connection)

    result = database_connection.query_schema()
    assert result == [
        Schema(
            name=f'{test_prefix}user',
            properties=[
                PropertySchema(name='email', type=str, required=False),
                PropertySchema(name='id', type=int, required=False),
            ],
            indexes=[],
            constraints=[],
        )
    ]


def test_update_property(database_connection: ElasticsearchConnection, test_prefix: str) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    result = database_connection.query_schema()
    assert result == [
        Schema(
            name=f'{test_prefix}user',
            properties=[
                PropertySchema(name='age', type=int, required=False),
                PropertySchema(name='email', type=str, required=False),
                PropertySchema(name='id', type=int, required=False),
            ],
            indexes=[],
            constraints=[],
        )
    ]

    update_age_property(database_connection)

    result = database_connection.query_schema()
    assert result == [
        Schema(
            name=f'{test_prefix}user',
            properties=[
                PropertySchema(name='age', type=str, required=False),
                PropertySchema(name='email', type=str, required=False),
                PropertySchema(name='id', type=int, required=False),
            ],
            indexes=[],
            constraints=[],
        )
    ]


def test_add_constraint(database_connection: ElasticsearchConnection, test_prefix: str) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    result = database_connection.query_schema()
    assert result == [
        Schema(
            name=f'{test_prefix}user',
            properties=[
                PropertySchema(name='age', type=int, required=False),
                PropertySchema(name='email', type=str, required=False),
                PropertySchema(name='id', type=int, required=False),
            ],
            indexes=[],
            constraints=[],
        )
    ]

    add_unique_constraint(database_connection)

    result = database_connection.query_schema()
    assert len(result) == 1
    schema = result[0]
    assert schema.name == f'{test_prefix}user'
    assert schema.constraints is not None
    assert len(schema.constraints) == 1
    assert schema.constraints[0].name == 'uk_user_email_unique'
    assert schema.constraints[0].fields == ['email', 'age']  # type: ignore[union-attr,attr-defined]


def test_drop_constraint(database_connection: ElasticsearchConnection) -> None:
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

    result = database_connection.query_schema()
    assert len(result) == 1
    schema = result[0]
    assert schema.constraints is not None
    assert len(schema.constraints) == 1
    assert schema.constraints[0].name == 'uk_user_email_unique'

    delete_unique_constraint(database_connection)

    result = database_connection.query_schema()
    assert len(result) == 1
    schema = result[0]
    assert schema.constraints is not None
    assert len(schema.constraints) == 0


def test_add_index(database_connection: ElasticsearchConnection) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    result = database_connection.query_schema()
    assert len(result) == 1
    schema = result[0]
    assert schema.indexes is not None
    assert len(schema.indexes) == 0

    add_index(database_connection)

    result = database_connection.query_schema()
    assert len(result) == 1
    schema = result[0]
    assert schema.indexes is not None
    assert len(schema.indexes) == 1
    assert schema.indexes[0].name == 'idx_user_email'
    assert schema.indexes[0].fields == ['email', 'age']


def test_delete_index(database_connection: ElasticsearchConnection) -> None:
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

    result = database_connection.query_schema()
    assert len(result) == 1
    schema = result[0]
    assert schema.indexes is not None
    assert len(schema.indexes) == 1
    assert schema.indexes[0].name == 'idx_user_email'

    delete_index(database_connection)

    result = database_connection.query_schema()
    assert len(result) == 1
    schema = result[0]
    assert schema.indexes is not None
    assert len(schema.indexes) == 0
