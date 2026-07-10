"""JsonbObject SQL emission on sqlite + postgres.

``JsonbObject`` carries ordered key -> expression pairs and renders as:
- ``json_object('k', ...)`` on SQLite
- ``jsonb_build_object('k', ...)`` on PostgreSQL
"""

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.select_expression import SelectExpression
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.jsonb_object import JsonbObject

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


def _q(gen: SqlGenerator, expr: JsonbObject) -> tuple[str, list]:
    return gen.compile_query(
        QueryStatement(only=[], expressions=[SelectExpression(expression=expr, alias='obj')], table=_TABLE)
    )


def test_jsonb_object_expression_renders_function_call_sqlite() -> None:
    expr = JsonbObject(
        pairs=[
            ('slug', _field_expr('Parent', 'slug')),
            ('realm', _field_expr('Parent', 'realm')),
        ]
    )

    sql, values = _q(_lite, expr)

    assert sql == (
        'SELECT json_object(\'slug\', "Parent"."slug", \'realm\', "Parent"."realm") AS "obj" FROM "Parent"'
    )
    assert values == []


def test_jsonb_object_expression_renders_function_call_postgres() -> None:
    expr = JsonbObject(
        pairs=[
            ('slug', _field_expr('Parent', 'slug')),
            ('realm', _field_expr('Parent', 'realm')),
        ]
    )

    sql, values = _q(_pg, expr)

    assert sql == (
        'SELECT jsonb_build_object(\'slug\', "Parent"."slug", \'realm\', "Parent"."realm") AS "obj" FROM "Parent"'
    )
    assert values == []


def test_jsonb_object_expression_single_pair() -> None:
    expr = JsonbObject(pairs=[('pk', _field_expr('Parent', 'pk'))])

    sql, _ = _q(_lite, expr)

    assert sql == 'SELECT json_object(\'pk\', "Parent"."pk") AS "obj" FROM "Parent"'


def test_jsonb_object_expression_preserves_key_order_from_mapping() -> None:
    # dict input is normalized to ordered pairs, preserving insertion order.
    expr = JsonbObject({'a': _field_expr('Parent', 'x'), 'b': _field_expr('Parent', 'y')})

    sql, _ = _q(_pg, expr)

    assert sql == (
        'SELECT jsonb_build_object(\'a\', "Parent"."x", \'b\', "Parent"."y") AS "obj" FROM "Parent"'
    )
