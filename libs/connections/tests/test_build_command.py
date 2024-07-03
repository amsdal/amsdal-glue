from amsdal_glue_connections.sql.sql_builders.command_builder import build_sql_data_command
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.data import DeleteData
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateData


def test_build_data_command__insert() -> None:
    sql, values = build_sql_data_command(
        mutation=InsertData(
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

    assert sql == 'INSERT INTO users (id, name) VALUES (?, ?), (?, ?)'
    assert values == [1, 'Alice', 2, 'Bob']


def test_build_data_command__update() -> None:
    sql, values = build_sql_data_command(
        mutation=UpdateData(
            schema=SchemaReference(name='users', version=Version.LATEST),
            data=Data(data={'role': 'staff'}),
            query=Conditions(
                Condition(
                    field=FieldReference(field=Field(name='is_active'), table_name='users'),
                    lookup=FieldLookup.EXACT,
                    value=Value(True),  # noqa: FBT003
                ),
            ),
        ),
    )

    assert sql == 'UPDATE users SET role = ? WHERE users.is_active IS ?'
    assert values == ['staff', True]


def test_build_data_command__delete() -> None:
    sql, values = build_sql_data_command(
        mutation=DeleteData(
            schema=SchemaReference(name='users', version=Version.LATEST),
            query=Conditions(
                Condition(
                    field=FieldReference(field=Field(name='is_active'), table_name='users'),
                    lookup=FieldLookup.EXACT,
                    value=Value(False),  # noqa: FBT003
                ),
            ),
        ),
    )

    assert sql == 'DELETE FROM users WHERE users.is_active IS ?'
    assert values == [False]
