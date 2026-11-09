"""What `parse_json_path_index_expression` accepts from each catalog, and what it refuses."""

import pytest
from amsdal_glue_core.common.enums import ScalarType

from amsdal_glue_connections.sql.connections.base_view_introspection import parse_json_path_index_expression
from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import _index_column_elements

_SQLITE_CASE = (
    "CASE WHEN json_type(\"evidence\"->'ref'->'object_id') = 'null' THEN NULL "
    "WHEN json_type(\"evidence\"->'ref'->'object_id') = 'text' "
    "THEN (\"evidence\"->'ref')->>'object_id' ELSE \"evidence\"->'ref'->'object_id' END"
)

_ACCEPTED = [
    ('postgresql', "((evidence -> 'ref'::text) ->> 'object_id'::text)", ScalarType.TEXT),
    ('postgresql', "((evidence -> 'ref'::text) -> 'object_id'::text)", ScalarType.JSONB),
    ('postgresql', "(((\"Evidence\" -> 'ref'::text) -> 'a'::text) ->> 'b'::text)", ScalarType.TEXT),
    ('sqlite', _SQLITE_CASE, ScalarType.TEXT),
    ('sqlite', f'({_SQLITE_CASE})', ScalarType.TEXT),
    ('sqlite', "(\"evidence\"->'ref')->>'object_id'", ScalarType.JSONB),
    ('sqlite', "((\"evidence\"->'ref')->>'object_id')", ScalarType.JSONB),
]


@pytest.mark.parametrize(('dialect', 'expression', 'output_type'), _ACCEPTED)
def test_recognised_forms(dialect: str, expression: str, output_type: ScalarType) -> None:
    parsed = parse_json_path_index_expression(expression, dialect)

    assert parsed is not None
    column, json_path, parsed_type = parsed
    assert column in {'evidence', 'Evidence'}
    assert json_path[0] == 'ref'
    assert parsed_type == output_type


def test_path_and_column_are_extracted() -> None:
    assert parse_json_path_index_expression("((evidence -> 'ref'::text) ->> 'object_id'::text)", 'postgresql') == (
        'evidence',
        ['ref', 'object_id'],
        ScalarType.TEXT,
    )
    assert parse_json_path_index_expression("((\"evidence\"->'ref')->>'object_id')", 'sqlite') == (
        'evidence',
        ['ref', 'object_id'],
        ScalarType.JSONB,
    )


@pytest.mark.parametrize(
    ('dialect', 'expression'),
    [
        ('postgresql', None),
        ('postgresql', ''),
        ('postgresql', 'lower(title)'),
        ('postgresql', '(lower(title))'),
        ('postgresql', "(evidence ->> 'a'::text)::integer"),
        ('postgresql', "((evidence ->> 'ref'::text) -> 'object_id'::text)"),
        ('postgresql', '(evidence -> 1)'),
        # `->` last is the JSON form on PostgreSQL, but SQLite never renders it, so it is not recognised.
        ('sqlite', "(\"evidence\"->'ref')->'object_id'"),
        ('sqlite', 'lower("title")'),
        (
            'sqlite',
            _SQLITE_CASE.replace("\"evidence\"->'ref')->>'object_id' ELSE", "\"other\"->'ref')->>'object_id' ELSE"),
        ),
        ('sqlite', _SQLITE_CASE.replace('THEN NULL', 'THEN 0')),
    ],
)
def test_other_expressions_are_not_recognised(dialect: str, expression: str | None) -> None:
    assert parse_json_path_index_expression(expression, dialect) is None


def test_index_column_elements_respect_nesting_and_quotes() -> None:
    ddl = f'CREATE INDEX "i" ON "t" (({_SQLITE_CASE}) DESC, "x, y" ASC, "z") WHERE "z" IN (1, 2)'

    assert _index_column_elements(ddl) == [f'({_SQLITE_CASE})', '"x, y"', '"z"']


def test_index_column_elements_without_ddl() -> None:
    assert _index_column_elements(None) == []
    assert _index_column_elements('') == []
