from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY


def _registry_query() -> QueryStatement:
    return QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))


def test__introspection_succeeds_after_reconnect_on_same_object(
    database_connection: SqliteConnection,
) -> None:
    """Reconnecting the SAME connection object must recreate the (per-connection) registry views.

    Previously a ``_views_created`` flag on the object suppressed view recreation on reconnect, so
    introspection failed with ``no such table: __amsdal__table_registry``. The flag is gone: the
    idempotent view DDL is re-issued on every introspection call.
    """
    db_path = database_connection._db_path  # noqa: SLF001

    database_connection.execute('CREATE TABLE widget (id INTEGER PRIMARY KEY, name TEXT)')

    # First introspection creates the temporary views for this connection.
    first = database_connection.query_schema(_registry_query())
    assert 'widget' in {schema.name for schema in first}

    # Reconnect the SAME object: the previous connection's temporary views are gone.
    database_connection.disconnect()
    database_connection.connect(db_path=db_path)

    # Must succeed by recreating the views, not raise "no such table".
    second = database_connection.query_schema(_registry_query())
    assert 'widget' in {schema.name for schema in second}
