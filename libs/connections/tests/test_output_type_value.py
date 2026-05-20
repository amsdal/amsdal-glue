"""Value placeholder rendering — output_type effect on emitted SQL.

Investigation findings (locked):
- sqlite: output_type=None + value is dict|list → 'json(?)'.
  output_type=None + other values → '?'. output_type is not None →
  routes through CAST: 'cast(? as TEXT)' for str, etc.
- postgres: output_type=None → '%s'. output_type is not None → 'cast(%s as TEXT)'.
"""

from datetime import datetime
from datetime import timezone

from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.connections.postgres_connection import get_pg_transform
from amsdal_glue_connections.sql.connections.sqlite_connection import get_sqlite_transform
from amsdal_glue_connections.sql.sql_builders.build_expression import build_expression


def test_value_string_output_type_none_emits_plain_placeholder_sqlite() -> None:
    sql, vals = build_expression(
        Value(value='2026-01-01', output_type=None),
        transform=get_sqlite_transform(),
    )

    assert sql == '?'
    assert vals == ['2026-01-01']


def test_value_string_output_type_str_emits_cast_text_sqlite() -> None:
    sql, vals = build_expression(
        Value(value='2026-01-01', output_type=str),
        transform=get_sqlite_transform(),
    )

    assert sql == 'cast(? as TEXT)'
    assert vals == ['2026-01-01']


def test_value_string_output_type_none_vs_str_postgres() -> None:
    sql_none, _ = build_expression(
        Value(value='2026-01-01', output_type=None),
        transform=get_pg_transform(),
    )
    sql_str, _ = build_expression(
        Value(value='2026-01-01', output_type=str),
        transform=get_pg_transform(),
    )

    assert sql_none == '%s'
    assert sql_str == '(%s)::TEXT'


def test_value_int_output_type_none_emits_plain_placeholder_sqlite() -> None:
    sql, vals = build_expression(
        Value(value=42, output_type=None),
        transform=get_sqlite_transform(),
    )

    assert sql == '?'
    assert vals == [42]


def test_value_int_output_type_int_emits_cast_integer_sqlite() -> None:
    sql, _ = build_expression(
        Value(value=42, output_type=int),
        transform=get_sqlite_transform(),
    )

    assert sql == 'cast(? as INTEGER)'


def test_value_datetime_output_type_none_emits_plain_placeholder_sqlite() -> None:
    dt = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    sql, vals = build_expression(
        Value(value=dt, output_type=None),
        transform=get_sqlite_transform(),
    )

    assert sql == '?'
    assert vals == [dt]


def test_value_datetime_output_type_str_emits_cast_text_sqlite() -> None:
    dt = datetime(2026, 1, 1, tzinfo=timezone.utc)
    sql, vals = build_expression(
        Value(value=dt, output_type=str),
        transform=get_sqlite_transform(),
    )

    assert sql == 'cast(? as TEXT)'
    assert vals == [dt]


def test_value_dict_output_type_none_wraps_with_json_sqlite() -> None:
    """sqlite-specific: dict/list values without explicit output_type are wrapped in json()."""
    sql, vals = build_expression(
        Value(value={'a': 1}, output_type=None),
        transform=get_sqlite_transform(),
    )

    assert sql == 'json(?)'
    assert vals == [{'a': 1}]
