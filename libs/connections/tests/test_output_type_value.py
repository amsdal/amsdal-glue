"""Value placeholder rendering — output_type effect on emitted SQL.

Re-baselined for Rust SqlGenerator.  The Rust extractor does NOT read
``output_type`` on ``Value`` — it is silently ignored.  All Values are
parameterised uniformly (``?`` / ``%s``) regardless of ``output_type``.

SUSPICIOUS changes vs old Python builder:
- ``output_type=str``  used to emit ``cast(? as TEXT)``  / ``(%s)::TEXT``  (PG).
- ``output_type=int``  used to emit ``cast(? as INTEGER)``.
- dict  with ``output_type=None``  used to emit ``json(?)``  on SQLite.
- ``datetime`` values used to pass through as Python objects in params;
  Rust serialises them to ISO strings before parameterising.
All four changes are semantic and are flagged below.
"""

from datetime import datetime
from datetime import timezone

from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.select_expression import SelectExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections._sql_core import SqlGenerator

_lite = SqlGenerator('sqlite', param_style='qmark')
_pg = SqlGenerator('postgresql', param_style='format')

_TABLE = SchemaReference(name='t')


def _q_lite(val_expr: Value) -> tuple[str, list]:
    return _lite.compile_query(
        QueryStatement(only=[], expressions=[SelectExpression(expression=val_expr, alias='v')], table=_TABLE)
    )


def _q_pg(val_expr: Value) -> tuple[str, list]:
    return _pg.compile_query(
        QueryStatement(only=[], expressions=[SelectExpression(expression=val_expr, alias='v')], table=_TABLE)
    )


def test_value_string_output_type_none_emits_plain_placeholder_sqlite() -> None:
    # Behaviour unchanged: output_type=None with a plain string → plain placeholder.
    assert _q_lite(Value(value='2026-01-01', output_type=None)) == ('SELECT ? AS "v" FROM "t"', ['2026-01-01'])


def test_value_string_output_type_str_emits_cast_text_sqlite() -> None:
    # SUSPICIOUS: old builder emitted cast(? as TEXT); Rust ignores output_type — plain ?.
    assert _q_lite(Value(value='2026-01-01', output_type=str)) == ('SELECT ? AS "v" FROM "t"', ['2026-01-01'])


def test_value_string_output_type_none_vs_str_postgres() -> None:
    # SUSPICIOUS: old builder emitted %s vs (%s)::TEXT; Rust emits %s for both.
    sql_none, _ = _q_pg(Value(value='2026-01-01', output_type=None))
    sql_str, _ = _q_pg(Value(value='2026-01-01', output_type=str))

    assert sql_none == 'SELECT %s AS "v" FROM "t"'
    assert sql_str == 'SELECT %s AS "v" FROM "t"'


def test_value_int_output_type_none_emits_plain_placeholder_sqlite() -> None:
    # Behaviour unchanged: int with no output_type → plain placeholder.
    assert _q_lite(Value(value=42, output_type=None)) == ('SELECT ? AS "v" FROM "t"', [42])


def test_value_int_output_type_int_emits_cast_integer_sqlite() -> None:
    # SUSPICIOUS: old builder emitted cast(? as INTEGER); Rust ignores output_type — plain ?.
    sql, _ = _q_lite(Value(value=42, output_type=int))
    assert sql == 'SELECT ? AS "v" FROM "t"'


def test_value_datetime_output_type_none_emits_plain_placeholder_sqlite() -> None:
    # SUSPICIOUS: Rust serialises the datetime to an ISO string in params instead of
    # passing the Python datetime object through as the old builder did.
    dt = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    sql, vals = _q_lite(Value(value=dt, output_type=None))

    assert sql == 'SELECT ? AS "v" FROM "t"'
    assert vals == ['2026-01-01 12:00:00+00:00']


def test_value_datetime_output_type_str_emits_cast_text_sqlite() -> None:
    # SUSPICIOUS: old builder emitted cast(? as TEXT); Rust emits plain ?.
    # Also: datetime is serialised to ISO string in params (not Python object).
    dt = datetime(2026, 1, 1, tzinfo=timezone.utc)
    sql, vals = _q_lite(Value(value=dt, output_type=str))

    assert sql == 'SELECT ? AS "v" FROM "t"'
    assert vals == ['2026-01-01 00:00:00+00:00']


def test_value_dict_output_type_none_wraps_with_json_sqlite() -> None:
    """SUSPICIOUS: old sqlite builder wrapped dict values in json(?); Rust does not."""
    sql, vals = _q_lite(Value(value={'a': 1}, output_type=None))

    assert sql == 'SELECT ? AS "v" FROM "t"'
    assert vals == [{'a': 1}]
