"""Build helpers for golden-master SQL characterization tests.

Each helper turns a glue AST node into the exact (sql, params) the current
string-concatenation builders produce, for one dialect. The returned tuple is
asserted against a captured literal in the feature tests.
"""
from typing import Any

from amsdal_glue_connections.sql.connections.postgres_connection import get_pg_transform
from amsdal_glue_connections.sql.connections.postgres_connection.base import PostgresConnectionMixin
from amsdal_glue_connections.sql.connections.sqlite_connection import get_sqlite_transform
from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import SqliteConnection
from amsdal_glue_connections.sql.sql_builders.command_builder import build_sql_data_command
from amsdal_glue_connections.sql.sql_builders.query_builder import build_sql_query
from amsdal_glue_connections.sql.sql_builders.schema_builder import build_schema_mutation

# PostgresConnectionMixin._to_sql_type is an instance method (not a staticmethod/classmethod),
# so we instantiate once and bind the method for use as a type_transform callable.
_pg_mixin = PostgresConnectionMixin()


def pg(query: Any) -> tuple[str, list[Any]]:
    return build_sql_query(query=query, transform=get_pg_transform())


def lite(query: Any) -> tuple[str, list[Any]]:
    return build_sql_query(query=query, transform=get_sqlite_transform())


def pg_cmd(mutation: Any) -> tuple[str, list[Any]]:
    return build_sql_data_command(mutation=mutation, transform=get_pg_transform())


def lite_cmd(mutation: Any) -> tuple[str, list[Any]]:
    return build_sql_data_command(mutation=mutation, transform=get_sqlite_transform())


def pg_ddl(mutation: Any) -> list[tuple[str, list[Any]]]:
    return build_schema_mutation(
        mutation,
        type_transform=_pg_mixin._to_sql_type,
        transform=get_pg_transform(),
    )


def lite_ddl(mutation: Any) -> list[tuple[str, list[Any]]]:
    return build_schema_mutation(
        mutation,
        type_transform=SqliteConnection.to_sql_type,
        transform=get_sqlite_transform(),
    )
