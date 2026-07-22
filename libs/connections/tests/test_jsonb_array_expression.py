"""JsonbArray SQL emission on sqlite + postgres.

Model rename: ``JsonbArrayExpression`` → ``JsonbArray`` (a ``Func`` subclass).

On SQLite the JSON lowering rewrites the array constructor to
``jsonb_array(CASE WHEN json_valid(col) = 1 THEN jsonb(col) ELSE col END, ...)`` --
the same shape main's ``func_transform`` produced, which preserves the JSON structure
of pre-parsed columns. Postgres emits ``jsonb_build_array(...)`` unchanged.
"""

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.select_expression import SelectExpression
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.jsonb_array import JsonbArray

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
    # SQLite maps the array constructor to jsonb_array with the json_valid CASE WHEN
    # wrapping per element -- main's func_transform shape (preserves pre-parsed JSON).
    expr = JsonbArray(
        items=[
            _field_expr('Parent', 'slug'),
            _field_expr('Parent', 'realm'),
        ]
    )

    sql, values = _q(_lite, expr)

    assert sql == (
        'SELECT jsonb_array('
        'CASE WHEN json_valid("Parent"."slug") = 1 THEN jsonb("Parent"."slug") ELSE "Parent"."slug" END, '
        'CASE WHEN json_valid("Parent"."realm") = 1 THEN jsonb("Parent"."realm") ELSE "Parent"."realm" END'
        ') AS "arr" FROM "Parent"'
    )
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
    expr = JsonbArray(items=[_field_expr('Parent', 'pk')])

    sql, _ = _q(_lite, expr)

    assert sql == (
        'SELECT jsonb_array('
        'CASE WHEN json_valid("Parent"."pk") = 1 THEN jsonb("Parent"."pk") ELSE "Parent"."pk" END'
        ') AS "arr" FROM "Parent"'
    )


def test_jsonb_array_expression_empty_items() -> None:
    """Edge case: sqlite emits `jsonb_array()` (no args)."""
    expr = JsonbArray(items=[])

    sql, _ = _q(_lite, expr)

    assert sql == 'SELECT jsonb_array() AS "arr" FROM "Parent"'
