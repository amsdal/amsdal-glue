from decimal import Decimal

from amsdal_glue_core.common.data_models.schema import DecimalSchemaModel

from amsdal_glue_connections.sql.connections.sqlite_connection.base import SqliteConnectionMixin
from amsdal_glue_connections.sql.sql_builders.sqlite_utils.value_transform import sqlite_value_transform


def test_sqlite_decimal_value_to_str() -> None:
    assert sqlite_value_transform(Decimal('12.50')) == '12.50'


def test_sqlite_decimal_schema_to_text_affinity() -> None:
    sql = SqliteConnectionMixin.to_sql_type(DecimalSchemaModel(precision=10, scale=2))
    assert 'TEXT' in sql  # TEXT affinity preserves exact string storage
    assert sql == 'DECIMAL_TEXT(10, 2)'
    assert SqliteConnectionMixin.to_sql_type(DecimalSchemaModel(precision=None, scale=None)) == 'DECIMAL_TEXT'


def test_sqlite_decimal_decltype_round_trips() -> None:
    conn = SqliteConnectionMixin()
    result = conn.to_python_type('DECIMAL_TEXT(10, 2)')
    assert isinstance(result, DecimalSchemaModel)
    assert result.precision == 10
    assert result.scale == 2

    unconstrained = conn.to_python_type('DECIMAL_TEXT')
    assert isinstance(unconstrained, DecimalSchemaModel)
    assert unconstrained.precision is None
    assert unconstrained.scale is None
