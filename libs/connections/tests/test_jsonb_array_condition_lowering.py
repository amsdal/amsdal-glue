"""JsonbArray in a WHERE/JOIN condition on SQLite must round-trip against a JSON-text column.

The historical metadata join compiles to ``object_id = json_array(pk_col...)``. On SQLite each
``json_array`` argument is otherwise treated as an opaque scalar, so a composite-PK / reference
column whose TEXT holds a JSON object (``{"ref": {...}}``) is double-escaped instead of embedded,
and the stored ``object_id`` (written with ``json.dumps`` spacing) never text-equals the minified
``jsonb_array(...)`` output. The SQLite lowering must therefore:
  * wrap each ``jsonb_array`` item as ``CASE WHEN json_valid(col) THEN jsonb(col) ELSE col END`` so a
    JSON-text column embeds as structure while a plain scalar is left untouched, and
  * wrap the compared column in ``jsonb()`` so both sides are canonicalised.
``jsonb()`` canonicalises spacing, so existing spaced ``json.dumps`` rows still match.
Postgres compares ``jsonb`` natively and must stay untouched.
"""

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.jsonb_array import JsonbArray

_lite = SqlGenerator('sqlite', param_style='qmark')
_pg = SqlGenerator('postgresql', param_style='format')

_TABLE = SchemaReference(name='PostTags')


def _field(table: str, name: str) -> FieldReferenceExpression:
    return FieldReferenceExpression(field_reference=FieldReference(field=Field(name=name), table_name=table))


def _query(gen: SqlGenerator) -> str:
    stmt = QueryStatement(
        table=_TABLE,
        where=Conditions(
            Condition(
                left=_field('Meta', 'object_id'),
                lookup=FieldLookup.EQ,
                right=JsonbArray(items=[_field('PostTags', 'post'), _field('PostTags', 'tag')]),
            ),
        ),
    )
    sql, _ = gen.compile_query(stmt)
    return sql


def test_sqlite_json_array_condition_unwraps_items_and_normalises_column() -> None:
    sql = _query(_lite)

    assert (
        'WHERE jsonb("Meta"."object_id") = jsonb_array('
        'CASE WHEN json_valid("PostTags"."post") = 1 THEN jsonb("PostTags"."post") ELSE "PostTags"."post" END, '
        'CASE WHEN json_valid("PostTags"."tag") = 1 THEN jsonb("PostTags"."tag") ELSE "PostTags"."tag" END)'
    ) in sql


def test_postgres_json_array_condition_unchanged() -> None:
    sql = _query(_pg)

    assert 'WHERE "Meta"."object_id" = jsonb_build_array("PostTags"."post", "PostTags"."tag")' in sql


def _nested_field(table: str, *path: str) -> FieldReferenceExpression:
    """A `->`/`->>` extraction, e.g. ``team->'ref'->>'object_id'`` for path ('team','ref','object_id')."""
    field = Field(name=path[-1])
    for name in reversed(path[:-1]):
        field = Field(name=name, child=field)
    return FieldReferenceExpression(field_reference=FieldReference(field=field, table_name=table))


def test_sqlite_json_array_vs_json_extraction_wraps_extraction_in_jsonb() -> None:
    """The composite-PK reverse-FK join: ``team->'ref'->>'object_id' = jsonb_array(pk...)``.

    The extraction yields the JSON TEXT of the array; the array lowers to a JSONB blob. The extraction
    side MUST be wrapped in ``jsonb()`` too, or SQLite compares TEXT to BLOB and the join finds nothing
    -- the regression this test guards.
    """
    stmt = QueryStatement(
        table=_TABLE,
        where=Conditions(
            Condition(
                left=_nested_field('Rel', 'team', 'ref', 'object_id'),
                lookup=FieldLookup.EQ,
                right=JsonbArray(items=[_field('T', 'org_id'), _field('T', 'team_code')]),
            ),
        ),
    )
    sql, _ = _lite.compile_query(stmt)

    assert (
        'WHERE jsonb(("Rel"."team"->\'ref\')->>\'object_id\') = jsonb_array('
        'CASE WHEN json_valid("T"."org_id") = 1 THEN jsonb("T"."org_id") ELSE "T"."org_id" END, '
        'CASE WHEN json_valid("T"."team_code") = 1 THEN jsonb("T"."team_code") ELSE "T"."team_code" END)'
    ) in sql
