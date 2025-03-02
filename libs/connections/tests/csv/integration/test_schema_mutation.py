from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.csv_connection import CsvConnection
from tests.csv.testcases.schema_mutations import create_user_schema
from tests.csv.testcases.schema_mutations import DEFAULT_SCHEMA
from tests.csv.testcases.schema_mutations import delete_user_schema
from tests.csv.testcases.schema_mutations import rename_user_schema


def test_create_schema(database_connection: CsvConnection) -> None:
    create_user_schema(database_connection)

    assert database_connection.query_schema() == [
        Schema(
            name='user',
            version=Version.LATEST,
            properties=[
                PropertySchema(name='id', type=str, required=False),
                PropertySchema(name='email', type=str, required=False),
                PropertySchema(name='age', type=str, required=False),
                PropertySchema(name='first_name', type=str, required=False),
                PropertySchema(name='last_name', type=str, required=False),
            ],
        )
    ]


def test_rename_schema(database_connection: CsvConnection) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert database_connection.query_schema() == [
        Schema(
            name='user',
            version=Version.LATEST,
            properties=[
                PropertySchema(name='id', type=str, required=False),
                PropertySchema(name='email', type=str, required=False),
                PropertySchema(name='age', type=str, required=False),
            ],
        )
    ]
    rename_user_schema(database_connection)

    assert database_connection.query_schema() == [
        Schema(
            name='customer',
            version=Version.LATEST,
            properties=[
                PropertySchema(name='id', type=str, required=False),
                PropertySchema(name='email', type=str, required=False),
                PropertySchema(name='age', type=str, required=False),
            ],
        )
    ]


def test_delete_schema(database_connection: CsvConnection) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=DEFAULT_SCHEMA),
            ],
        ),
    )

    assert database_connection.query_schema() == [
        Schema(
            name='user',
            version=Version.LATEST,
            properties=[
                PropertySchema(name='id', type=str, required=False),
                PropertySchema(name='email', type=str, required=False),
                PropertySchema(name='age', type=str, required=False),
            ],
        )
    ]

    delete_user_schema(database_connection)

    assert database_connection.query_schema() == []
