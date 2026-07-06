"""End-to-end tests for the join-based ``query_schema`` registry feature on SQLite.

These exercise the full pipeline: build a ``QueryStatement`` that starts from the
table registry, INNER JOINs a metadata registry view, filters on a registry column,
and gets back the full ``Schema`` objects of the matching tables.
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

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
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


def test__query_schema_by_datetime_property(database_connection: SqliteConnection) -> None:
    database_connection.execute('CREATE TABLE orders (id INTEGER PRIMARY KEY, created_at DATETIME, total DECIMAL)')
    database_connection.execute('CREATE TABLE events (id INTEGER PRIMARY KEY, happened_at DATETIME)')
    database_connection.execute('CREATE TABLE plain (id INTEGER PRIMARY KEY, label TEXT)')

    query = _registry_query(TABLE_PROPERTY_REGISTRY, 'type', 'DATETIME')
    schemas = database_connection.query_schema(query)

    assert {schema.name for schema in schemas} == {'orders', 'events'}


def test__query_schema_by_unique_constraint(database_connection: SqliteConnection) -> None:
    database_connection.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT UNIQUE)')
    database_connection.execute('CREATE TABLE orders (id INTEGER PRIMARY KEY, total DECIMAL)')

    query = _registry_query(TABLE_CONSTRAINT_REGISTRY, 'type', 'u')
    schemas = database_connection.query_schema(query)

    assert {schema.name for schema in schemas} == {'users'}
