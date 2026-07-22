"""End-to-end tests for the join-based ``query_schema`` registry feature on Postgres.

Mirrors ``sqlite_connection/integration/test_schema_query_join.py``: the same
QueryStatement shape (start from the table registry, INNER JOIN a metadata
registry view, filter on a registry column) returns the full ``Schema`` objects
of the matching tables. The constraint-registry ``type`` codes ('p'/'u'/'f') are
identical across back-ends, so that test is byte-for-byte the same query as SQLite.
"""

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_CONSTRAINT_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_PROPERTY_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY


def _fref(name: str, table: str) -> FieldReferenceExpression:
    return FieldReferenceExpression(field_reference=FieldReference(field=Field(name=name), table_name=table))


def _registry_query(registry: str, type_field: str, type_value: object) -> QueryStatement:
    """Schemas of all tables that have a matching row in ``registry``.

    Joins ``<registry>.table_name`` to ``__amsdal__table_registry.name`` and filters
    ``<registry>.<type_field> == type_value``.
    """
    return QueryStatement(
        table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST),
        joins=[
            JoinQuery(
                table=SchemaReference(name=registry, version=Version.LATEST),
                on=Conditions(
                    Condition(
                        left=_fref('name', TABLE_REGISTRY),
                        lookup=FieldLookup.EQ,
                        right=_fref('table_name', registry),
                    )
                ),
                join_type=JoinType.INNER,
            )
        ],
        where=Conditions(
            Condition(
                left=_fref(type_field, registry),
                lookup=FieldLookup.EQ,
                right=Value(type_value),
            )
        ),
    )


def test__query_schema_by_datetime_property(database_connection: PostgresConnection) -> None:
    database_connection.execute('CREATE TABLE orders (id SERIAL PRIMARY KEY, created_at TIMESTAMP, total NUMERIC)')
    database_connection.execute('CREATE TABLE events (id SERIAL PRIMARY KEY, happened_at TIMESTAMP)')
    database_connection.execute('CREATE TABLE plain (id SERIAL PRIMARY KEY, label TEXT)')

    # information_schema.columns.data_type for a bare TIMESTAMP column.
    query = _registry_query(TABLE_PROPERTY_REGISTRY, 'type', 'timestamp without time zone')
    schemas = database_connection.query_schema(query)

    assert {schema.name for schema in schemas} == {'orders', 'events'}


def test__query_schema_by_unique_constraint(database_connection: PostgresConnection) -> None:
    database_connection.execute('CREATE TABLE users (id SERIAL PRIMARY KEY, email TEXT UNIQUE)')
    database_connection.execute('CREATE TABLE orders (id SERIAL PRIMARY KEY, total NUMERIC)')

    query = _registry_query(TABLE_CONSTRAINT_REGISTRY, 'type', 'u')
    schemas = database_connection.query_schema(query)

    assert {schema.name for schema in schemas} == {'users'}
