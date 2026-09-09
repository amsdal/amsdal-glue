from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import DataInput
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.from_values import FromValues
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.data import UpdateData

from ._harness import lite_cmd
from ._harness import pg_cmd


def test_update_with_from_values_pg() -> None:
    mutation = UpdateData(
        schema=SchemaReference(name='orders', version=Version.LATEST),
        data=DataInput(
            data={
                'user_id': FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='id'), table_name='_cascade_parent'),
                ),
            },
        ),
        query=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='user_id'), table_name='orders'),
                ),
                lookup=FieldLookup.EQ,
                right=FieldReferenceExpression(
                    field_reference=FieldReference(
                        field=Field(name='$__planner__old_id'),
                        table_name='_cascade_parent',
                    ),
                ),
            ),
        ),
        from_tables=[
            FromValues(
                rows=[
                    [Value(value=1), Value(value=101)],
                    [Value(value=2), Value(value=102)],
                ],
                alias='_cascade_parent',
                columns=['$__planner__old_id', 'id'],
            ),
        ],
        returning=[FieldReference(field=Field(name='*'), table_name='')],
    )
    assert pg_cmd(mutation) == (
        (
            'UPDATE "orders" SET "user_id" = "_cascade_parent"."id"'
            ' FROM (VALUES (%s, %s), (%s, %s)) AS "_cascade_parent" ("$__planner__old_id", "id")'
            ' WHERE "orders"."user_id" = "_cascade_parent"."$__planner__old_id"'
            ' RETURNING *'
        ),
        [1, 101, 2, 102],
    )


def test_update_with_from_values_sqlite() -> None:
    mutation = UpdateData(
        schema=SchemaReference(name='orders', version=Version.LATEST),
        data=DataInput(
            data={
                'user_id': FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='id'), table_name='_cascade_parent'),
                ),
            },
        ),
        query=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='user_id'), table_name='orders'),
                ),
                lookup=FieldLookup.EQ,
                right=FieldReferenceExpression(
                    field_reference=FieldReference(
                        field=Field(name='$__planner__old_id'),
                        table_name='_cascade_parent',
                    ),
                ),
            ),
        ),
        from_tables=[
            FromValues(
                rows=[
                    [Value(value=1), Value(value=101)],
                ],
                alias='_cascade_parent',
                columns=['$__planner__old_id', 'id'],
            ),
        ],
        returning=[FieldReference(field=Field(name='*'), table_name='')],
    )
    # SQLite does not support (VALUES ...) AS t(cols) directly; the generator
    # rewrites it as SELECT col1 AS name1, col2 AS name2 FROM (VALUES (...)).
    assert lite_cmd(mutation) == (
        (
            'UPDATE "orders" SET "user_id" = "_cascade_parent"."id"'
            ' FROM (SELECT column1 AS "$__planner__old_id", column2 AS "id"'
            ' FROM (VALUES (?, ?))) AS "_cascade_parent"'
            ' WHERE "orders"."user_id" = "_cascade_parent"."$__planner__old_id"'
            ' RETURNING *'
        ),
        [1, 101],
    )
