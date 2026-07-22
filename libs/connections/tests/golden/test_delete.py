from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.data import DeleteData

from ._harness import lite_cmd
from ._harness import pg_cmd


def test_delete_with_where_sqlite() -> None:
    m = DeleteData(
        schema=SchemaReference(name='users', version=Version.LATEST),
        query=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='id'), table_name='users'),
                ),
                lookup=FieldLookup.EQ,
                right=Value(value=5),
            ),
        ),
    )
    # SQLite uses ANSI double-quoted identifiers.
    assert lite_cmd(m) == ('DELETE FROM "users" WHERE "users"."id" = ?', [5])


def test_delete_without_where_sqlite() -> None:
    m = DeleteData(schema=SchemaReference(name='users', version=Version.LATEST))
    # SQLite uses ANSI double-quoted identifiers.
    assert lite_cmd(m) == ('DELETE FROM "users"', [])


def test_delete_with_where_pg() -> None:
    m = DeleteData(
        schema=SchemaReference(name='users', version=Version.LATEST),
        query=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='id'), table_name='users'),
                ),
                lookup=FieldLookup.EQ,
                right=Value(value=5),
            ),
        ),
    )
    assert pg_cmd(m) == ('DELETE FROM "users" WHERE "users"."id" = %s', [5])


def test_delete_without_where_pg() -> None:
    m = DeleteData(schema=SchemaReference(name='users', version=Version.LATEST))
    assert pg_cmd(m) == ('DELETE FROM "users"', [])
