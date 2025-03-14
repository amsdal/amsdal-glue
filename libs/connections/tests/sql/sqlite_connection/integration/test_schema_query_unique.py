from unittest.mock import ANY

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint


def test__inline_unique_field_returned(database_connection: SqliteConnection) -> None:
    create_table_sql = """
        create table members
        (
            memb_id  INTEGER
                primary key,
            username VARCHAR(50)  not null,
            email    VARCHAR(100) not null
                unique
        );
    """
    database_connection.execute(create_table_sql)

    props, constraints, indexes = database_connection.get_table_info('members')
    unique_constraints = [
        constraint
        for constraint in constraints
        if isinstance(constraint, UniqueConstraint)
    ]
    assert unique_constraints == [
        UniqueConstraint(
            name=ANY,
            fields=['email'],
            condition=None,
        ),
    ]
