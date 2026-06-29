# ruff: noqa: SLF001
from decimal import Decimal

from amsdal_glue_core.common.data_models.schema import DecimalSchemaModel

from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import PostgresConnection
from amsdal_glue_connections.sql.sql_builders.postgres_utils.type_transform import pg_value_type_transform


def test_pg_bare_decimal_falls_back_to_numeric() -> None:
    assert pg_value_type_transform(Decimal) == 'NUMERIC'


def test_pg_decimal_schema_model_to_numeric() -> None:
    conn = PostgresConnection()
    assert conn._to_sql_type(DecimalSchemaModel(precision=10, scale=2)) == 'NUMERIC(10, 2)'
    assert conn._to_sql_type(DecimalSchemaModel(precision=None, scale=None)) == 'NUMERIC'


def test_pg_numeric_introspects_to_decimal_schema_model() -> None:
    conn = PostgresConnection()
    # typmod for NUMERIC(10,2) == ((precision << 16) | scale) + 4
    typmod = ((10 << 16) | 2) + 4
    result = conn._to_python_type('NUMERIC', None, {'typmod': typmod})
    assert isinstance(result, DecimalSchemaModel)
    assert result.precision == 10
    assert result.scale == 2


def test_pg_double_precision_still_float() -> None:
    conn = PostgresConnection()
    assert conn._to_python_type('DOUBLE PRECISION', None, {}) is float


def test_pg_build_column_update_numeric_uses_cast() -> None:
    conn = PostgresConnection()
    from amsdal_glue_core.common.data_models.schema import PropertySchema

    column = PropertySchema(name='amount', type=DecimalSchemaModel(precision=10, scale=2), required=True)
    stmt = conn._build_column_update(column)
    assert 'TYPE NUMERIC(10, 2)' in stmt
    assert 'USING "amount"::NUMERIC(10, 2)' in stmt
