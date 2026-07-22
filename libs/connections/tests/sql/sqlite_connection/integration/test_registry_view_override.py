"""The registry-view hook must be overridable per subclass/instance, and introspection must resolve
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

from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY


def test_registry_view_override_resolves_by_table_name(database_connection):
    # A versioned/lakehouse-style override: the registry view's `name` is the MODEL name (physical
    # name minus a `__v__<ver>` suffix) while `table_name` stays the physical table name.
    database_connection.execute('CREATE TABLE "orders__v__abc" ("id" INTEGER PRIMARY KEY)')

    override = dict(type(database_connection)._REGISTRY_VIEW_SQL)  # noqa: SLF001
    override[TABLE_REGISTRY] = (
        f'CREATE TEMPORARY VIEW IF NOT EXISTS "{TABLE_REGISTRY}" AS '  # noqa: S608
        "SELECT CASE WHEN instr(name, '__v__') > 0 THEN substr(name, 1, instr(name, '__v__') - 1) "
        'ELSE name END AS name, '
        "name AS table_name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    )
    database_connection._REGISTRY_VIEW_SQL = override  # instance override of the class attribute  # noqa: SLF001

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
