from unittest.mock import ANY

from amsdal_glue_core.common.data_models.constraints import UniqueConstraint

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection


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

    _, constraints, _ = database_connection.get_table_info('members')
    unique_constraints = [constraint for constraint in constraints if isinstance(constraint, UniqueConstraint)]
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

    _, constraints, _ = database_connection.get_table_info('members')
    unique_constraints = [constraint for constraint in constraints if isinstance(constraint, UniqueConstraint)]
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

    _, constraints, _ = database_connection.get_table_info('Fixture')
    unique_constraints = [constraint for constraint in constraints if isinstance(constraint, UniqueConstraint)]
    assert unique_constraints == [
        UniqueConstraint(
            name=ANY,
            fields=['external_id'],
            condition=None,
        ),
    ]
