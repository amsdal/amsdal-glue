"""``IndexField(json_path=..., output_type=...)``: an expression index over a path inside a JSON column.

The index expression must be the one a condition on that path renders -- otherwise the planner does not
use the index. Both are therefore built by the same code, and these tests pin that they stay equal.
"""

import re

import pytest
from amsdal_glue_connections._sql_core import InvalidValueError
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.schema import AddIndex

from ._harness import lite
from ._harness import lite_ddl
from ._harness import pg
from ._harness import pg_ddl

_REF = SchemaReference(name='passage', version=Version.LATEST)
_PATH = ['ref', 'object_id']


def _add_index(*fields: IndexField) -> AddIndex:
    return AddIndex(schema_ref=_REF, index=IndexSchema(name='idx_passage_evidence', fields=list(fields)))


def _json_field(output_type: ScalarType | None, **kwargs) -> IndexField:
    return IndexField(name='evidence', json_path=_PATH, output_type=output_type, **kwargs)


def _filter_expression(render, output_type: ScalarType | None, path: list[str] = _PATH) -> str:
    """The text of ``evidence -> path`` as the left side of ``=`` in a ``WHERE`` clause, without the qualifier."""
    field = Field(name=path[-1])
    for name in reversed(path[:-1]):
        field = Field(name=name, child=field)
    field = Field(name='evidence', child=field)

    statement = QueryStatement(
        table=_REF,
        where=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(field=field, table_name=''),
                    output_type=output_type,
                ),
                lookup=FieldLookup.EQ,
                right=Value('x'),
            ),
        ),
    )
    sql, _ = render(statement)
    return re.sub(r'^.* WHERE ', '', sql).rsplit(' = ', 1)[0]


@pytest.mark.parametrize('output_type', [ScalarType.TEXT, ScalarType.JSONB])
def test_pg_index_renders_the_expression_of_a_filter_on_that_path(output_type: ScalarType) -> None:
    ((sql, params),) = pg_ddl(_add_index(_json_field(output_type)))

    assert params == []
    expected = _filter_expression(pg, output_type)
    assert sql == f'CREATE INDEX "idx_passage_evidence" ON "passage" USING btree ({_wrap(expected)} ASC)'


@pytest.mark.parametrize('output_type', [ScalarType.TEXT, ScalarType.JSONB])
def test_sqlite_index_renders_the_expression_of_a_filter_on_that_path(output_type: ScalarType) -> None:
    ((sql, params),) = lite_ddl(_add_index(_json_field(output_type)))

    assert params == []
    expected = _filter_expression(lite, output_type)
    assert sql == f'CREATE INDEX "idx_passage_evidence" ON "passage" ({_wrap(expected)} ASC)'


def _wrap(expression: str) -> str:
    """Index expressions are always parenthesised; a filter's may already be."""
    return expression if _balanced_outer(expression) else f'({expression})'


def _balanced_outer(expression: str) -> bool:
    if not (expression.startswith('(') and expression.endswith(')')):
        return False
    depth = 0
    for index, char in enumerate(expression):
        depth += char == '('
        depth -= char == ')'
        if depth == 0:
            return index == len(expression) - 1
    return False


def test_pg_text_form() -> None:
    assert pg_ddl(_add_index(_json_field(ScalarType.TEXT))) == [
        (
            'CREATE INDEX "idx_passage_evidence" ON "passage" '
            "USING btree (((\"evidence\"->'ref')->>'object_id') ASC)",
            [],
        ),
    ]


def test_pg_jsonb_form() -> None:
    assert pg_ddl(_add_index(_json_field(ScalarType.JSONB))) == [
        (
            'CREATE INDEX "idx_passage_evidence" ON "passage" USING btree (("evidence"->\'ref\'->\'object_id\') ASC)',
            [],
        ),
    ]


def test_sqlite_text_form() -> None:
    assert lite_ddl(_add_index(_json_field(ScalarType.TEXT))) == [
        (
            'CREATE INDEX "idx_passage_evidence" ON "passage" '
            "((CASE WHEN json_type(\"evidence\"->'ref'->'object_id') "
            "= 'null' THEN NULL WHEN json_type(\"evidence\"->'ref'->'object_id') = 'text' "
            "THEN (\"evidence\"->'ref')->>'object_id' ELSE \"evidence\"->'ref'->'object_id' END) ASC)",
            [],
        ),
    ]


def test_sqlite_jsonb_form() -> None:
    assert lite_ddl(_add_index(_json_field(ScalarType.JSONB))) == [
        (
            'CREATE INDEX "idx_passage_evidence" ON "passage" ((("evidence"->\'ref\')->>\'object_id\') ASC)',
            [],
        ),
    ]


def test_pg_json_path_field_mixed_with_columns_keeps_declared_order() -> None:
    first = _add_index(IndexField(name='label'), _json_field(ScalarType.TEXT, direction=OrderDirection.DESC))
    last = _add_index(_json_field(ScalarType.TEXT), IndexField(name='label', direction=OrderDirection.DESC))

    assert pg_ddl(first)[0][0].endswith('("label" ASC, (("evidence"->\'ref\')->>\'object_id\') DESC)')
    assert pg_ddl(last)[0][0].endswith('((("evidence"->\'ref\')->>\'object_id\') ASC, "label" DESC)')


def test_create_table_creates_the_expression_index() -> None:
    from amsdal_glue_core.common.data_models.schema import PropertySchema
    from amsdal_glue_core.common.data_models.schema import Schema
    from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

    schema = Schema(
        name='passage',
        version=Version.LATEST,
        properties=[PropertySchema(name='evidence', type=ScalarType.JSONB, required=False)],
        indexes=[IndexSchema(name='idx_passage_evidence', fields=[_json_field(ScalarType.TEXT)])],
    )
    statements = pg_ddl(RegisterSchema(schema_ref=_REF, schema=schema))

    assert statements[-1][0] == (
        'CREATE INDEX "idx_passage_evidence" ON "passage" USING btree ((("evidence"->\'ref\')->>\'object_id\') ASC)'
    )


def test_a_plain_column_field_is_unchanged() -> None:
    assert pg_ddl(_add_index(IndexField(name='label'))) == [
        ('CREATE INDEX "idx_passage_evidence" ON "passage" USING btree ("label" ASC)', []),
    ]


@pytest.mark.parametrize('generate', [pg_ddl, lite_ddl])
@pytest.mark.parametrize(
    ('name', 'json_path'),
    [
        ('evidence"); DROP TABLE t; --', _PATH),
        ('evidence', ['ref', "object_id'); DROP TABLE t; --"]),
        ('evidence', ['ref', 'object id']),
        ('evidence', ['']),
    ],
)
def test_names_spliced_into_ddl_are_validated(generate, name: str, json_path: list[str]) -> None:
    field = IndexField(name=name, json_path=json_path, output_type=ScalarType.TEXT)

    with pytest.raises(InvalidValueError):
        generate(_add_index(field))
