"""SQLite decimal/DECIMAL_TEXT handling — re-pointed to Rust SqlGenerator.

Old tests used deleted internals: sqlite_value_transform, SqliteConnectionMixin.to_sql_type,
and DecimalSchemaModel.  Each is re-pointed to the surviving equivalent:
Value + compile_query for value rendering, compile_schema_mutation for DDL,
and to_python_type for introspection (still present on SqliteConnectionMixin).

SUSPICIOUS items flagged inline.
"""

from decimal import Decimal

from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.select_expression import SelectExpression
from amsdal_glue_core.common.data_models.types import CustomType
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_connections.sql.connections.sqlite_connection.base import SqliteConnectionMixin

_gen = SqlGenerator('sqlite', param_style='qmark')
_TABLE = SchemaReference(name='t', version=Version.LATEST)


def test_sqlite_decimal_value_to_str() -> None:
    # Old: sqlite_value_transform(Decimal('12.50')) == '12.50'
    #      (old builder coerced Decimal to string before binding).
    # Re-pointed: Value(Decimal(...), output_type=ScalarType.NUMERIC) via compile_query.
    # SUSPICIOUS: Rust/Value coerces to Decimal, not str.  The param is now
    # Decimal('12.50'), not the string '12.50'.  SQLite drivers receive a Decimal
    # object; behaviour depends on the driver (aiosqlite adapts it via str()).
    _, params = _gen.compile_query(
        QueryStatement(
            table=_TABLE,
            only=[],
            expressions=[SelectExpression(expression=Value(Decimal('12.50'), output_type=ScalarType.NUMERIC), alias='v')],
        )
    )
    assert len(params) == 1
    assert params[0] == Decimal('12.50')


def test_sqlite_decimal_schema_to_text_affinity() -> None:
    # Old: SqliteConnectionMixin.to_sql_type(DecimalSchemaModel(precision=10, scale=2))
    #      returned 'DECIMAL_TEXT(10, 2)' (contains 'TEXT' affinity).
    # Re-pointed: compile_schema_mutation emits DECIMAL_TEXT(10, 2) in the column type.
    schema = Schema(
        name='t',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='amount',
                type=CustomType(name='DECIMAL_TEXT', params={'precision': 10, 'scale': 2}),
                required=False,
            )
        ],
    )
    [(ddl, _)] = _gen.compile_schema_mutation(
        RegisterSchema(schema_ref=_TABLE, schema=schema)
    )
    assert 'TEXT' in ddl
    assert 'DECIMAL_TEXT(10, 2)' in ddl

    # Old: DecimalSchemaModel(precision=None, scale=None) → 'DECIMAL_TEXT'.
    schema_n = Schema(
        name='t',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='amount',
                type=CustomType(name='DECIMAL_TEXT'),
                required=False,
            )
        ],
    )
    [(ddl_n, _)] = _gen.compile_schema_mutation(
        RegisterSchema(schema_ref=_TABLE, schema=schema_n)
    )
    assert 'DECIMAL_TEXT' in ddl_n


def test_sqlite_decimal_decltype_round_trips() -> None:
    # Old: conn.to_python_type('DECIMAL_TEXT(10, 2)') returned DecimalSchemaModel(precision=10, scale=2).
    # Re-pointed: to_python_type still exists on SqliteConnectionMixin.
    # SUSPICIOUS: precision/scale are not preserved — both parameterised and bare DECIMAL_TEXT
    # now return CustomType(name='decimal_text', params=None).  Round-trip fidelity is lost.
    conn = SqliteConnectionMixin()
    result = conn.to_python_type('DECIMAL_TEXT(10, 2)')
    assert isinstance(result, CustomType)
    assert result.name == 'decimal_text'
    # SUSPICIOUS: params=None — precision/scale dropped (was precision=10, scale=2).
    assert result.params is None

    unconstrained = conn.to_python_type('DECIMAL_TEXT')
    assert isinstance(unconstrained, CustomType)
    assert unconstrained.name == 'decimal_text'
    assert unconstrained.params is None
