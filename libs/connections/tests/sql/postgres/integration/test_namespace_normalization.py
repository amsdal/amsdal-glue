"""PostgreSQL introspection must return the canonical ``namespace=None`` for the default schema.

Introspection stamped the connection's schema onto every returned ``Schema``, so a default-schema table
read back as ``namespace='public'`` while the rest of the stack (canonical constants, SQLite
introspection, every registered model, and main's own PG introspection) authors ``None``.
``Schema.__eq__`` compares ``namespace`` raw, so ``'public' != None`` flipped whole-schema equality and
aborted migration with ``NotImplementedError``. The fix normalises the default schema to ``None`` while
preserving a genuinely non-default schema.

The default-schema test FAILS on the ``'public'``-stamping code and PASSES after the fix; the
non-default test guards against over-collapsing every namespace to ``None``.
"""

import uuid

from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY

from .conftest import create_postgres_database
from .conftest import delete_postgres_database


def _all_tables_query() -> QueryStatement:
    return QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))


def test_default_schema_introspects_namespace_none(database_connection: PostgresConnection) -> None:
    """A table registered on the default (``public``) schema introspects with ``namespace=None``."""
    database_connection.execute('CREATE TABLE "widget" ("id" serial PRIMARY KEY, "name" text)')
    database_connection.execute('CREATE INDEX "widget_name_idx" ON "widget" ("name")')

    schemas = database_connection.introspect_schema(_all_tables_query())
    by_name = {s.name: s for s in schemas}

    assert 'widget' in by_name, f'widget not found; got {sorted(by_name)}'
    assert by_name['widget'].namespace is None


def test_non_default_schema_preserves_namespace() -> None:
    """A table under a genuinely non-default schema still introspects with its real namespace."""
    db_name = uuid.uuid4().hex
    db_host, db_port, db_user, db_password = create_postgres_database(db_name)

    connection = PostgresConnection()
    connection.connect(
        dsn=f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',
        schema='foo',
    )
    try:
        connection.execute('CREATE SCHEMA IF NOT EXISTS foo')
        connection.execute('CREATE TABLE foo.gadget (id serial PRIMARY KEY, name text)')

        schemas = connection.introspect_schema(_all_tables_query())
        by_name = {s.name: s for s in schemas}

        assert 'gadget' in by_name, f'gadget not found; got {sorted(by_name)}'
        assert by_name['gadget'].namespace == 'foo'
    finally:
        connection.disconnect()
        delete_postgres_database(db_name)
