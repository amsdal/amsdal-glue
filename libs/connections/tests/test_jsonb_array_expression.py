"""JsonbArrayExpression SQL emission on sqlite + postgres.

On postgres it emits `jsonb_build_array(col1, col2, ...)` unchanged.
On sqlite the func_transform rewrites it to `jsonb_array(CASE WHEN json_valid(col) THEN jsonb(col) ELSE col END, ...)`.
"""

from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.jsonb_array import JsonbArrayExpression

from amsdal_glue_connections.sql.connections.postgres_connection import get_pg_transform
from amsdal_glue_connections.sql.connections.sqlite_connection import get_sqlite_transform
from amsdal_glue_connections.sql.sql_builders.build_expression import build_expression


def _field_expr(table: str, name: str) -> FieldReferenceExpression:
    return FieldReferenceExpression(
        field_reference=FieldReference(
            field=Field(name=name),
            table_name=table,
        )
    )


def test_jsonb_array_expression_renders_function_call_sqlite() -> None:
    expr = JsonbArrayExpression(
        items=[
            _field_expr('Parent', 'slug'),
            _field_expr('Parent', 'realm'),
        ]
    )

    sql, values = build_expression(expr, transform=get_sqlite_transform())

    assert sql == (
        'jsonb_array('
        "CASE WHEN json_valid('Parent'.'slug') THEN jsonb('Parent'.'slug') ELSE 'Parent'.'slug' END, "
        "CASE WHEN json_valid('Parent'.'realm') THEN jsonb('Parent'.'realm') ELSE 'Parent'.'realm' END"
        ')'
    )
    assert values == []


def test_jsonb_array_expression_renders_function_call_postgres() -> None:
    expr = JsonbArrayExpression(
        items=[
            _field_expr('Parent', 'slug'),
            _field_expr('Parent', 'realm'),
        ]
    )

    sql, values = build_expression(expr, transform=get_pg_transform())

    assert sql == 'jsonb_build_array("Parent"."slug", "Parent"."realm")'
    assert values == []


def test_jsonb_array_expression_single_item() -> None:
    expr = JsonbArrayExpression(items=[_field_expr('Parent', 'pk')])

    sql, _ = build_expression(expr, transform=get_sqlite_transform())

    assert sql == ("jsonb_array(CASE WHEN json_valid('Parent'.'pk') THEN jsonb('Parent'.'pk') ELSE 'Parent'.'pk' END)")


def test_jsonb_array_expression_empty_items() -> None:
    """Edge case: sqlite emits `jsonb_array()` (no args), not `jsonb_build_array()`."""
    expr = JsonbArrayExpression(items=[])

    sql, _ = build_expression(expr, transform=get_sqlite_transform())

    assert sql == 'jsonb_array()'
