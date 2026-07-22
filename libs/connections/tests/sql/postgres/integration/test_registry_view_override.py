"""The Postgres registry-view builder must be overridable, and ``introspect_schema`` must resolve
physical tables by ``table_name`` -- the two prerequisites for a versioned (lakehouse) connection that
exposes a MODEL ``name`` distinct from the physical ``table_name``.
"""

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from psycopg import sql

from amsdal_glue_connections.sql.connections.postgres_connection.base import build_registry_view_sql
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY


def test_registry_view_override_resolves_by_table_name(database_connection):
    database_connection.execute('CREATE TABLE "orders__v__abc" ("id" INT PRIMARY KEY)')

    def override(schema):
        views = build_registry_view_sql(schema)
        views[TABLE_REGISTRY] = sql.SQL(
            'CREATE OR REPLACE TEMPORARY VIEW {view} AS '
            "SELECT CASE WHEN position('__v__' in table_name) > 0 "
            "THEN substring(table_name from 1 for position('__v__' in table_name) - 1) "
            'ELSE table_name END AS name, table_name '
            'FROM information_schema.tables '
            "WHERE table_schema = {schema} AND table_type = 'BASE TABLE'"
        ).format(view=sql.Identifier(TABLE_REGISTRY), schema=sql.Literal(schema))
        return views

    database_connection._build_registry_view_sql = override  # instance override  # noqa: SLF001

    # Filter by the MODEL name -> must still resolve the physical `orders__v__abc` (by `table_name`).
    query = QueryStatement(
        table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST),
        where=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='name'), table_name=TABLE_REGISTRY),
                ),
                lookup=FieldLookup.EQ,
                right=Value('orders'),
            ),
        ),
    )

    schemas = database_connection.query_schema(query)

    assert [schema.name for schema in schemas] == ['orders__v__abc']
