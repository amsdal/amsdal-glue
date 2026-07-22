"""Value placeholder rendering — what ``output_type`` does to a bound parameter.

``output_type`` on a ``Value`` types the PARAMETER, not the SQL: the placeholder stays a plain
``?`` / ``%s``. Emitting a SQL cast is the job of the separate ``Cast`` expression; ``output_type``
never emits a cast (``cast(? as TEXT)``, ``(%s)::TEXT``).

What the type does reach is the value that gets bound:
- a scalar type coerces the Python value (``42`` stays an ``int``, ``'2026-01-01'`` a ``str``);
- ``JSON``/``JSONB`` hands the connection a ``JsonValue`` marker, which psycopg binds as
  ``Jsonb(...)`` and SQLite serialises with ``json.dumps`` — see ``json_output_type_cases``.

A ``datetime`` is serialised to an ISO string before it is parameterised.
"""

from datetime import datetime
from datetime import timezone

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.select_expression import SelectExpression
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.expressions.value import Value

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


def test_value_string_output_type_str_emits_plain_placeholder_sqlite() -> None:
    # output_type does not cast: the placeholder is plain and the param keeps its type.
    result = _q_lite(Value(value='2026-01-01', output_type=ScalarType.TEXT))
    assert result == ('SELECT ? AS "v" FROM "t"', ['2026-01-01'])


def test_value_string_output_type_none_vs_str_postgres() -> None:
    # Neither form casts — an explicit `Cast` expression is what emits `::TEXT`.
    sql_none, _ = _q_pg(Value(value='2026-01-01', output_type=None))
    sql_str, _ = _q_pg(Value(value='2026-01-01', output_type=ScalarType.TEXT))

    assert sql_none == 'SELECT %s AS "v" FROM "t"'
    assert sql_str == 'SELECT %s AS "v" FROM "t"'


def test_value_int_output_type_none_emits_plain_placeholder_sqlite() -> None:
    # Behaviour unchanged: int with no output_type → plain placeholder.
    assert _q_lite(Value(value=42, output_type=None)) == ('SELECT ? AS "v" FROM "t"', [42])


def test_value_int_output_type_int_emits_cast_integer_sqlite() -> None:
    # output_type is ignored here; the param is a plain ?.
    sql, _ = _q_lite(Value(value=42, output_type=ScalarType.INTEGER))
    assert sql == 'SELECT ? AS "v" FROM "t"'


def test_value_datetime_output_type_none_emits_plain_placeholder_sqlite() -> None:
    # The datetime is serialised to an ISO string in params, not passed through as a Python object.
    dt = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    sql, vals = _q_lite(Value(value=dt, output_type=None))

    assert sql == 'SELECT ? AS "v" FROM "t"'
    assert vals == ['2026-01-01T12:00:00+00:00']


def test_value_datetime_output_type_str_emits_plain_placeholder_sqlite() -> None:
    # No cast, and the datetime is serialised to an ISO string in params.
    dt = datetime(2026, 1, 1, tzinfo=timezone.utc)
    sql, vals = _q_lite(Value(value=dt, output_type=ScalarType.TEXT))

    assert sql == 'SELECT ? AS "v" FROM "t"'
    assert vals == ['2026-01-01 00:00:00+00:00']


def test_value_dict_binds_as_a_json_parameter_sqlite() -> None:
    """A dict is JSON by construction, so it reaches the connection as a JSON-typed parameter.

    The marker is what lets the connection bind it (``json.dumps`` here, ``Jsonb(...)`` on psycopg)
    without having to guess from the Python type -- guessing only ever worked for dict and list.
    """
    from amsdal_glue_core.common.data_models.json_value import JsonValue

    sql, vals = _q_lite(Value(value={'a': 1}, output_type=None))

    assert sql == 'SELECT ? AS "v" FROM "t"'
    assert vals == [JsonValue({'a': 1}, ScalarType.JSONB)]
