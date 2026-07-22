from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import DataInput
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.data import DeleteData
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateData

_gen = SqlGenerator('sqlite', param_style='qmark')


def test_build_data_command__insert() -> None:
    sql, values = _gen.compile_mutation(
        InsertData(
            schema=SchemaReference(name='users', version=Version.LATEST),
            data=[
                DataInput(
                    data={
                        'id': 1,
                        'name': 'Alice',
                    },
                ),
                DataInput(
                    data={
                        'id': 2,
                        'name': 'Bob',
                    },
                ),
            ],
        ),
    )

    # SQLite identifiers use ANSI double-quotes.
    assert sql == 'INSERT INTO "users" ("id", "name") VALUES (?, ?), (?, ?)'
    assert values == [1, 'Alice', 2, 'Bob']


def test_build_data_command_with_namespace__insert() -> None:
    sql, values = _gen.compile_mutation(
        InsertData(
            schema=SchemaReference(name='users', namespace='ns1', version=Version.LATEST),
            data=[
                DataInput(
                    data={
                        'id': 1,
                        'name': 'Alice',
                    },
                ),
                DataInput(
                    data={
                        'id': 2,
                        'name': 'Bob',
                    },
                ),
            ],
        ),
    )

    # Double-quotes for identifiers.
    assert sql == 'INSERT INTO "ns1"."users" ("id", "name") VALUES (?, ?), (?, ?)'
    assert values == [1, 'Alice', 2, 'Bob']


def test_build_data_command__update() -> None:
    # UpdateData.data is a DataInput: a row of expressions on the way IN.
    sql, values = _gen.compile_mutation(
        UpdateData(
            schema=SchemaReference(name='users', version=Version.LATEST),
            data=DataInput(data={'role': Value('staff')}),
            query=Conditions(
                Condition(
                    left=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='is_active'), table_name='users')
                    ),
                    lookup=FieldLookup.EXACT,
                    right=Value(True),  # noqa: FBT003
                ),
            ),
        ),
    )

    # Double-quoted identifiers; EXACT emits = (not IS).
    assert sql == 'UPDATE "users" SET "role" = ? WHERE "users"."is_active" = ?'
    assert values == ['staff', True]


def test_build_data_command_with_namespace__update() -> None:
    sql, values = _gen.compile_mutation(
        UpdateData(
            schema=SchemaReference(name='users', namespace='ns1', version=Version.LATEST),
            data=DataInput(data={'role': Value('staff')}),
            query=Conditions(
                Condition(
                    left=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='is_active'), table_name='users')
                    ),
                    lookup=FieldLookup.EXACT,
                    right=Value(True),  # noqa: FBT003
                ),
            ),
        ),
    )

    assert sql == 'UPDATE "ns1"."users" SET "role" = ? WHERE "users"."is_active" = ?'
    assert values == ['staff', True]


def test_build_data_command_with_namespaces__update() -> None:
    sql, values = _gen.compile_mutation(
        UpdateData(
            schema=SchemaReference(name='users', namespace='ns1', version=Version.LATEST),
            data=DataInput(data={'role': Value('staff')}),
            query=Conditions(
                Condition(
                    left=FieldReferenceExpression(
                        field_reference=FieldReference(
                            field=Field(name='is_active'), table_name='users', namespace='ns1'
                        )
                    ),
                    lookup=FieldLookup.EXACT,
                    right=Value(True),  # noqa: FBT003
                ),
            ),
        ),
    )

    assert sql == 'UPDATE "ns1"."users" SET "role" = ? WHERE "ns1"."users"."is_active" = ?'
    assert values == ['staff', True]


def test_build_data_command__delete() -> None:
    sql, values = _gen.compile_mutation(
        DeleteData(
            schema=SchemaReference(name='users', version=Version.LATEST),
            query=Conditions(
                Condition(
                    left=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='is_active'), table_name='users')
                    ),
                    lookup=FieldLookup.EXACT,
                    right=Value(False),  # noqa: FBT003
                ),
            ),
        ),
    )

    assert sql == 'DELETE FROM "users" WHERE "users"."is_active" = ?'
    assert values == [False]


def test_build_data_command_with_namespace__delete() -> None:
    sql, values = _gen.compile_mutation(
        DeleteData(
            schema=SchemaReference(name='users', namespace='ns1', version=Version.LATEST),
            query=Conditions(
                Condition(
                    left=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='is_active'), table_name='users')
                    ),
                    lookup=FieldLookup.EXACT,
                    right=Value(False),  # noqa: FBT003
                ),
            ),
        ),
    )

    assert sql == 'DELETE FROM "ns1"."users" WHERE "users"."is_active" = ?'
    assert values == [False]


def test_build_data_command_with_namespaces__delete() -> None:
    sql, values = _gen.compile_mutation(
        DeleteData(
            schema=SchemaReference(name='users', namespace='ns1', version=Version.LATEST),
            query=Conditions(
                Condition(
                    left=FieldReferenceExpression(
                        field_reference=FieldReference(
                            field=Field(name='is_active'), table_name='users', namespace='ns1'
                        )
                    ),
                    lookup=FieldLookup.EXACT,
                    right=Value(False),  # noqa: FBT003
                ),
            ),
        ),
    )

    assert sql == 'DELETE FROM "ns1"."users" WHERE "ns1"."users"."is_active" = ?'
    assert values == [False]
