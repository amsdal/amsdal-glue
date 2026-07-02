"""JsonbArray SQL emission on sqlite + postgres.

Re-baselined for Rust SqlGenerator.

Model rename: ``JsonbArrayExpression`` → ``JsonbArray`` (a ``Func`` subclass).

SUSPICIOUS — SQLite dialect differences vs old Python builder:
- Old builder: ``jsonb_array(CASE WHEN json_valid(col) THEN jsonb(col) ELSE col END, ...)``.
  The CASE WHEN was a func_transform rewrite to handle pre-parsed JSON columns.
- Rust generator: ``json_array(col1, col2, ...)`` — no CASE WHEN, and uses
  ``json_array`` (text-JSON) instead of ``jsonb_array`` (binary-JSON).
  These are semantically different: if a column already contains a JSON string the
  old builder preserved structure; the Rust generator does not.

Postgres is unchanged: both old and new emit ``jsonb_build_array(...)``.
"""

from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.select_expression import SelectExpression
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.jsonb_array import JsonbArray

from amsdal_glue_connections._sql_core import SqlGenerator

_lite = SqlGenerator('sqlite', param_style='qmark')
_pg = SqlGenerator('postgresql', param_style='format')

_TABLE = SchemaReference(name='Parent')


def _field_expr(table: str, name: str) -> FieldReferenceExpression:
    return FieldReferenceExpression(
        field_reference=FieldReference(
            field=Field(name=name),
            table_name=table,
        )
    )


def _q(gen: SqlGenerator, expr: JsonbArray) -> tuple[str, list]:
    return gen.compile_query(
        QueryStatement(only=[], expressions=[SelectExpression(expression=expr, alias='arr')], table=_TABLE)
    )


def test_jsonb_array_expression_renders_function_call_sqlite() -> None:
    # SUSPICIOUS: Rust emits json_array (text-JSON, no CASE WHEN) instead of
    # the old jsonb_array(CASE WHEN json_valid(col) THEN jsonb(col) ELSE col END, ...).
    expr = JsonbArray(
        items=[
            _field_expr('Parent', 'slug'),
            _field_expr('Parent', 'realm'),
        ]
    )

    sql, values = _q(_lite, expr)

    assert sql == 'SELECT json_array("Parent"."slug", "Parent"."realm") AS "arr" FROM "Parent"'
    assert values == []


def test_jsonb_array_expression_renders_function_call_postgres() -> None:
    # Postgres output unchanged (jsonb_build_array); now via compile_query.
    expr = JsonbArray(
        items=[
            _field_expr('Parent', 'slug'),
            _field_expr('Parent', 'realm'),
        ]
    )

    sql, values = _q(_pg, expr)

    assert sql == 'SELECT jsonb_build_array("Parent"."slug", "Parent"."realm") AS "arr" FROM "Parent"'
    assert values == []


def test_jsonb_array_expression_single_item() -> None:
    # SUSPICIOUS: Rust emits json_array (not jsonb_array CASE WHEN ...).
    expr = JsonbArray(items=[_field_expr('Parent', 'pk')])

    sql, _ = _q(_lite, expr)

    assert sql == 'SELECT json_array("Parent"."pk") AS "arr" FROM "Parent"'


def test_jsonb_array_expression_empty_items() -> None:
    """Edge case: sqlite emits `json_array()` (no args)."""
    # SUSPICIOUS: old emitted jsonb_array(); Rust emits json_array().
    expr = JsonbArray(items=[])

    sql, _ = _q(_lite, expr)

    assert sql == 'SELECT json_array() AS "arr" FROM "Parent"'
