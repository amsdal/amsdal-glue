"""End-to-end execution of the Power (**) and BitwiseXor (^) operators on SQLite.

The golden tests assert the generated SQL text; these tests run that SQL against a
real SQLite database (including the ``executemany`` batching path) to prove the
emitted forms — ``power(?, ?)`` for ``**`` and the ``(a|b)-(a&b)`` expansion for
``^`` — are valid and numerically correct.
"""

import sqlite3

import pytest
from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.select_expression import SelectExpression
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.data import UpdateItem
from amsdal_glue_core.common.operations.mutations.data import UpdateManyData

_gen = SqlGenerator('sqlite', param_style='qmark')


@pytest.fixture()
def db() -> sqlite3.Connection:
    conn = sqlite3.connect(':memory:')
    yield conn
    conn.close()


def _eval(db: sqlite3.Connection, expr) -> object:
    """Compile ``expr`` as a scalar SELECT and execute it, returning the value."""
    sql, params = _gen.compile_query(
        QueryStatement(
            only=[],
            expressions=[SelectExpression(expression=expr, alias='v')],
            table=SchemaReference(name='_'),
        )
    )
    scalar_sql = sql.split(' FROM ')[0]  # drop the dummy FROM — a bare SELECT
    return db.execute(scalar_sql, params).fetchone()[0]


def test_power_executes_on_sqlite(db: sqlite3.Connection) -> None:
    assert _eval(db, Value(2) ** Value(3)) == 8
    assert _eval(db, Value(5) ** Value(2)) == 25


@pytest.mark.parametrize(
    ('a', 'b'),
    [(5, 3), (10, 6), (255, 128), (0, 0), (1, 1), (12345, 6789)],
)
def test_bitwise_xor_matches_native_xor_on_sqlite(db: sqlite3.Connection, a: int, b: int) -> None:
    assert _eval(db, Value(a) ^ Value(b)) == (a ^ b)


def _id_eq(value: int) -> Conditions:
    return Conditions(
        Condition(
            left=FieldReferenceExpression(field_reference=FieldReference(field=Field(name='id'), table_name='t')),
            lookup=FieldLookup.EQ,
            right=Value(value),
        )
    )


def test_bitwise_xor_executemany_batches_correctly(db: sqlite3.Connection) -> None:
    """UpdateMany with a ``^`` expression groups into one SQL template and executes;
    each operand is bound twice (the expansion references it twice), params stay aligned."""
    db.execute('CREATE TABLE t (id INTEGER PRIMARY KEY, a INTEGER, b INTEGER, r INTEGER)')
    rows = [(1, 5, 3), (2, 10, 6), (3, 255, 128)]
    db.executemany('INSERT INTO t (id, a, b, r) VALUES (?, ?, ?, 0)', rows)

    mutation = UpdateManyData(
        schema=SchemaReference(name='t'),
        items=[UpdateItem(data={'r': Value(a) ^ Value(b)}, query=_id_eq(i)) for i, a, b in rows],
    )
    grouped = mutation.compile_grouped(_gen)

    # All items share the same SQL shape → exactly one group.
    assert len(grouped) == 1
    sql, param_sets = grouped[0]
    assert sql == 'UPDATE "t" SET "r" = (((?) | (?)) - ((?) & (?))) WHERE "t"."id" = ?'
    assert param_sets == [[5, 3, 5, 3, 1], [10, 6, 10, 6, 2], [255, 128, 255, 128, 3]]

    db.executemany(sql, param_sets)

    for i, a, b in rows:
        stored = db.execute('SELECT r FROM t WHERE id = ?', (i,)).fetchone()[0]
        assert stored == (a ^ b)
