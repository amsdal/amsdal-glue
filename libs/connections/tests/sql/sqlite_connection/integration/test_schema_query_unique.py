from unittest.mock import ANY

from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY


def _query_unique_constraints(database_connection: SqliteConnection, table_name: str) -> list[UniqueConstraint]:
    # Real introspection path (public query_schema), replacing the removed legacy get_table_info.
    # Returns the UNIQUE constraints reflected for ``table_name``.
    query = QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
    schemas = [schema for schema in database_connection.query_schema(query) if schema.name == table_name]
    constraints = schemas[0].constraints or [] if schemas else []
    return [constraint for constraint in constraints if isinstance(constraint, UniqueConstraint)]


def test__inline_unique_field_returned(database_connection: SqliteConnection) -> None:
    create_table_sql = """
        create table members
        (
            memb_id  INTEGER
                primary key,
            username VARCHAR(50)  not null,
            email    VARCHAR(100)
                unique
        );
    """
    database_connection.execute(create_table_sql)

    unique_constraints = _query_unique_constraints(database_connection, 'members')
    assert unique_constraints == [
        UniqueConstraint(
            name=ANY,
            fields=['email'],
            condition=None,
        ),
    ]


def test__inline_unique_field_not_null_returned(database_connection: SqliteConnection) -> None:
    create_table_sql = """
        create table members
        (
            memb_id  INTEGER
                primary key,
            username VARCHAR(50)  not null,
            email    VARCHAR(100)  not null
                unique
        );
    """
    database_connection.execute(create_table_sql)

    unique_constraints = _query_unique_constraints(database_connection, 'members')
    assert unique_constraints == [
        UniqueConstraint(
            name=ANY,
            fields=['email'],
            condition=None,
        ),
    ]


def test__without_inline_unique(database_connection: SqliteConnection) -> None:
    create_table_sql = (
        "CREATE TABLE 'Fixture' ('partition_key' TEXT NOT NULL, 'class_name' TEXT, 'external_id' TEXT NOT NULL, "
        "'data' JSONB NOT NULL, CONSTRAINT 'pk_fixture' PRIMARY KEY ('partition_key'), "
        "CONSTRAINT 'unq_fixture_external_id' UNIQUE ('external_id'))"
    )
    database_connection.execute(create_table_sql)

    unique_constraints = _query_unique_constraints(database_connection, 'Fixture')
    assert unique_constraints == [
        UniqueConstraint(
            name=ANY,
            fields=['external_id'],
            condition=None,
        ),
    ]
