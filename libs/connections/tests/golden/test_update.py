from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.data import UpdateData

from ._harness import lite_cmd
from ._harness import pg_cmd


def test_update_with_where_sqlite() -> None:
    m = UpdateData(
        schema=SchemaReference(name='users', version=Version.LATEST),
        data=Data(data={'role': 'staff'}),
        query=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='is_active'), table_name='users'),
                ),
                lookup=FieldLookup.EXACT,
                right=Value(value=True),
            ),
        ),
    )
    assert lite_cmd(m) == ("UPDATE 'users' SET 'role' = ? WHERE 'users'.'is_active' IS ?", ['staff', True])


def test_update_without_where_sqlite() -> None:
    m = UpdateData(
        schema=SchemaReference(name='users', version=Version.LATEST),
        data=Data(data={'role': 'staff'}),
    )
    assert lite_cmd(m) == ("UPDATE 'users' SET 'role' = ?", ['staff'])


def test_update_with_where_pg() -> None:
    m = UpdateData(
        schema=SchemaReference(name='users', version=Version.LATEST),
        data=Data(data={'role': 'staff'}),
        query=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='is_active'), table_name='users'),
                ),
                lookup=FieldLookup.EXACT,
                right=Value(value=True),
            ),
        ),
    )
    assert pg_cmd(m) == ('UPDATE "users" SET "role" = %s WHERE "users"."is_active" IS %s', ['staff', True])


def test_update_without_where_pg() -> None:
    m = UpdateData(
        schema=SchemaReference(name='users', version=Version.LATEST),
        data=Data(data={'role': 'staff'}),
    )
    assert pg_cmd(m) == ('UPDATE "users" SET "role" = %s', ['staff'])
