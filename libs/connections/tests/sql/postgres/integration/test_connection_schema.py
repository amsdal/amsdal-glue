import uuid

from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY

from .conftest import create_postgres_database
from .conftest import delete_postgres_database


def test__introspection_uses_connection_schema_not_public() -> None:
    """Introspection must read the CONNECTION's schema, and stamp that schema as the namespace.

    A table created in a non-``public`` schema (matching the connection's configured schema) is
    discovered and its ``Schema.namespace`` reflects the queried schema. On the old hardcoded
    ``'public'`` code this returned no tables (or the wrong namespace).
    """
    db_name = uuid.uuid4().hex
    db_host, db_port, db_user, db_password = create_postgres_database(db_name)

    connection = PostgresConnection()
    connection.connect(
        dsn=f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',
        schema='amsdal_test_ns',
    )

    try:
        connection.execute('CREATE SCHEMA IF NOT EXISTS amsdal_test_ns')
        connection.execute('CREATE TABLE amsdal_test_ns.widget (id serial PRIMARY KEY, name text)')

        schemas = connection.introspect_schema(
            QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST)),
        )

        by_name = {schema.name: schema for schema in schemas}
        assert 'widget' in by_name, f'widget not found; got {sorted(by_name)}'
        assert by_name['widget'].namespace == 'amsdal_test_ns'
        # A table left in public must NOT leak in through the connection schema filter.
        assert all(schema.namespace == 'amsdal_test_ns' for schema in schemas)
    finally:
        connection.disconnect()
        delete_postgres_database(db_name)
