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
from amsdal_glue_core.common.operations.mutations.data import DeleteData
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateData

from amsdal_glue_connections._sql_core import SqlGenerator

_gen = SqlGenerator('sqlite', param_style='qmark')


def test_build_data_command__insert() -> None:
    sql, values = _gen.compile_mutation(
        InsertData(
            schema=SchemaReference(name='users', version=Version.LATEST),
            data=[
                Data(
                    data={
                        'id': 1,
                        'name': 'Alice',
                    },
                ),
                Data(
                    data={
                        'id': 2,
                        'name': 'Bob',
                    },
                ),
            ],
        ),
    )

    # Re-baselined: SQLite identifiers use ANSI double-quotes (was single-quotes).
    assert sql == 'INSERT INTO "users" ("id", "name") VALUES (?, ?), (?, ?)'
    assert values == [1, 'Alice', 2, 'Bob']


def test_build_data_command_with_namespace__insert() -> None:
    sql, values = _gen.compile_mutation(
        InsertData(
            schema=SchemaReference(name='users', namespace='ns1', version=Version.LATEST),
            data=[
                Data(
                    data={
                        'id': 1,
                        'name': 'Alice',
                    },
                ),
                Data(
                    data={
                        'id': 2,
                        'name': 'Bob',
                    },
                ),
            ],
        ),
    )

    # Re-baselined: double-quotes for identifiers.
    assert sql == 'INSERT INTO "ns1"."users" ("id", "name") VALUES (?, ?), (?, ?)'
    assert values == [1, 'Alice', 2, 'Bob']


def test_build_data_command__update() -> None:
    # UpdateData.data is now dict[str, Expression], not a Data object.
    sql, values = _gen.compile_mutation(
        UpdateData(
            schema=SchemaReference(name='users', version=Version.LATEST),
            data={'role': Value('staff')},
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

    # Re-baselined: double-quotes; EXACT now emits = (was IS) — known different-but-valid.
    assert sql == 'UPDATE "users" SET "role" = ? WHERE "users"."is_active" = ?'
    assert values == ['staff', True]


def test_build_data_command_with_namespace__update() -> None:
    sql, values = _gen.compile_mutation(
        UpdateData(
            schema=SchemaReference(name='users', namespace='ns1', version=Version.LATEST),
            data={'role': Value('staff')},
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
            data={'role': Value('staff')},
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
