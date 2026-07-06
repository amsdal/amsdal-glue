"""End-to-end execution of the Power (**) and BitwiseXor (^) operators on Postgres.

Runs the emitted forms — ``l ^ r`` for ``**`` (Postgres ``^`` is exponentiation) and
``l # r`` for ``^`` (Postgres ``#`` is bitwise XOR) — against a real Postgres server
through the standard ``database_connection`` fixture (register schema, insert rows,
query a computed column). The ``executemany`` batching path
(``UpdateManyData.compile_grouped``) is exercised on the same live connection.
"""

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.select_expression import SelectExpression
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.combined import Combined
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateItem
from amsdal_glue_core.common.operations.mutations.data import UpdateManyData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection

_ROWS = [(1, 5, 3), (2, 10, 6), (3, 255, 128)]
_GEN = SqlGenerator('postgresql', param_style='format')


def _nums_ref() -> SchemaReference:
    return SchemaReference(name='nums', version=Version.LATEST)


def _ref(name: str) -> FieldReferenceExpression:
    return FieldReferenceExpression(field_reference=FieldReference(field=Field(name=name), table_name='nums'))


def _setup(connection: PostgresConnection) -> None:
    connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema_ref=_nums_ref(),
                    schema=Schema(
                        name='nums',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                            PropertySchema(name='a', type=ScalarType.INTEGER, required=False),
                            PropertySchema(name='b', type=ScalarType.INTEGER, required=False),
                            PropertySchema(name='r', type=ScalarType.INTEGER, required=False),
                        ],
                    ),
                )
            ]
        )
    )
    connection.run_mutations([
        InsertData(schema=_nums_ref(), data=[Data(data={'id': i, 'a': a, 'b': b, 'r': 0}) for i, a, b in _ROWS])
    ])


def _query(expr, alias: str) -> QueryStatement:
    return QueryStatement(
        table=_nums_ref(),
        only=[FieldReference(field=Field(name='id'), table_name='nums')],
        expressions=[SelectExpression(expression=expr, alias=alias)],
        order_by=[
            OrderByQuery(
                field=FieldReference(field=Field(name='id'), table_name='nums'),
                direction=OrderDirection.ASC,
            )
        ],
    )


def test_power_over_columns_executes(database_connection: PostgresConnection) -> None:
    _setup(database_connection)
    expr = Combined(left=_ref('a'), operator='**', right=_ref('b'))
    result = database_connection.query(_query(expr, 'p'))
    assert [float(row.data['p']) for row in result] == [float(a**b) for _, a, b in _ROWS]


def test_bitwise_xor_over_columns_matches_native(database_connection: PostgresConnection) -> None:
    _setup(database_connection)
    expr = Combined(left=_ref('a'), operator='^', right=_ref('b'))
    result = database_connection.query(_query(expr, 'x'))
    assert [row.data['x'] for row in result] == [a ^ b for _, a, b in _ROWS]


def _id_eq(value: int) -> Conditions:
    return Conditions(Condition(left=_ref('id'), lookup=FieldLookup.EQ, right=Value(value)))


def test_bitwise_xor_executemany_updates_live_rows(database_connection: PostgresConnection) -> None:
    _setup(database_connection)

    mutation = UpdateManyData(
        schema=_nums_ref(),
        items=[UpdateItem(data={'r': Value(a) ^ Value(b)}, query=_id_eq(i)) for i, a, b in _ROWS],
    )
    grouped = mutation.compile_grouped(_GEN)
    assert len(grouped) == 1
    sql, param_sets = grouped[0]
    with database_connection.connection.cursor() as cur:
        cur.executemany(sql, param_sets)

    result = database_connection.query(_query(_ref('r'), 'r'))
    assert [row.data['r'] for row in result] == [a ^ b for _, a, b in _ROWS]
