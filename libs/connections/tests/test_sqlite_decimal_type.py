"""SQLite decimal/DECIMAL_TEXT handling.

Uses Value + compile_query for value rendering, compile_schema_mutation for DDL,
and _sqlite_type_to_field_type for introspection (the real query_schema path).
"""

from decimal import Decimal

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.select_expression import SelectExpression
from amsdal_glue_core.common.data_models.types import DecimalType
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import _sqlite_type_to_field_type

_gen = SqlGenerator('sqlite', param_style='qmark')
_TABLE = SchemaReference(name='t', version=Version.LATEST)


def test_sqlite_decimal_value_to_str() -> None:
    # Value(Decimal(...), output_type=ScalarType.NUMERIC) via compile_query.
    # Rust/Value coerces to Decimal, not str.  The param is now
    # Decimal('12.50'), not the string '12.50'.  SQLite drivers receive a Decimal
    # object; behaviour depends on the driver (aiosqlite adapts it via str()).
    _, params = _gen.compile_query(
        QueryStatement(
            table=_TABLE,
            only=[],
            expressions=[
                SelectExpression(expression=Value(Decimal('12.50'), output_type=ScalarType.NUMERIC), alias='v')
            ],
        )
    )
    assert len(params) == 1
    assert params[0] == Decimal('12.50')


def test_sqlite_decimal_schema_to_text_affinity() -> None:
    #      returned 'DECIMAL_TEXT(10, 2)' (contains 'TEXT' affinity).
    # compile_schema_mutation emits DECIMAL_TEXT(10, 2) in the column type.
    schema = Schema(
        name='t',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='amount',
                type=DecimalType(precision=10, scale=2),
                required=False,
            )
        ],
    )
    [(ddl, _)] = _gen.compile_schema_mutation(RegisterSchema(schema_ref=_TABLE, schema=schema))
    assert 'TEXT' in ddl
    assert 'DECIMAL_TEXT(10, 2)' in ddl

    schema_n = Schema(
        name='t',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='amount',
                type=DecimalType(),
                required=False,
            )
        ],
    )
    [(ddl_n, _)] = _gen.compile_schema_mutation(RegisterSchema(schema_ref=_TABLE, schema=schema_n))
    assert 'DECIMAL_TEXT' in ddl_n


def test_sqlite_type_to_field_type_preserves_precision_scale() -> None:
    # _sqlite_type_to_field_type is used by query_schema/_introspect_columns to convert
    # the raw PRAGMA type string to a FieldType.
    result = _sqlite_type_to_field_type('DECIMAL_TEXT(10, 2)')
    assert result == DecimalType(precision=10, scale=2)

    # NUMERIC(p,s) introspects to the agnostic DecimalType so precision/scale survive round-trips.
    result_numeric = _sqlite_type_to_field_type('NUMERIC(10, 2)')
    assert result_numeric == DecimalType(precision=10, scale=2)

    # Bare NUMERIC (no params) stays as ScalarType.NUMERIC.
    assert _sqlite_type_to_field_type('NUMERIC') == ScalarType.NUMERIC


def test_sqlite_decimal_decltype_round_trips() -> None:
    # _sqlite_type_to_field_type (the real query_schema/_introspect_columns path) must preserve
    # precision/scale for faithful DECIMAL_TEXT round-trips.
    result = _sqlite_type_to_field_type('DECIMAL_TEXT(10, 2)')
    assert result == DecimalType(precision=10, scale=2)

    # Bare DECIMAL_TEXT (the SQLite rendering of DecimalType()) round-trips to DecimalType().
    unconstrained = _sqlite_type_to_field_type('DECIMAL_TEXT')
    assert unconstrained == DecimalType(precision=None, scale=None)
