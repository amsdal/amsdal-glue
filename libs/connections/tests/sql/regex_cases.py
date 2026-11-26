"""Shared dataset and cases for `regex` / `iregex` on a text column, run by the SQLite and PostgreSQL suites.

The pattern is a Python `re` string passed to the database unchanged: SQLite runs it with the `REGEXP`
function the connection registers (Python `re`), PostgreSQL with its own engine (`~` / `~*`). The cases check
what glue is responsible for, not the regex engines: a pattern reaches the database intact and `iregex` ignores
case on both. Each case is ``(case_id, QueryStatement, expected ids)``, the same on both databases.
"""

from typing import Any

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import DataInput
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

TABLE = 'RegexLookup'
SCHEMA_REF = SchemaReference(name=TABLE, version=Version.LATEST)

ROWS: list[dict[str, Any]] = [
    {'id': 1, 'text': 'John'},
    {'id': 2, 'text': 'john smith'},
    {'id': 3, 'text': 'johnny'},
    {'id': 4, 'text': 'Шлюз'},
    {'id': 5, 'text': "it's C.S.A"},
    {'id': 6, 'text': 'CxSxA'},
    {'id': 7, 'text': None},
]

SCHEMA_COMMAND = SchemaCommand(
    mutations=[
        RegisterSchema(
            schema_ref=SCHEMA_REF,
            schema=Schema(
                name=TABLE,
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=ScalarType.BIGINT, required=True),
                    PropertySchema(name='text', type=ScalarType.TEXT, required=False),
                ],
            ),
        ),
    ],
)

INSERT_ROWS: list[DataMutation] = [InsertData(schema=SCHEMA_REF, data=[DataInput(data=dict(row)) for row in ROWS])]


def match(lookup: FieldLookup, pattern: str | None, *, negated: bool = False) -> QueryStatement:
    text = FieldReferenceExpression(field_reference=FieldReference(field=Field(name='text'), table_name=TABLE))
    return QueryStatement(
        table=SCHEMA_REF,
        where=Conditions(Condition(left=text, lookup=lookup, right=Value(pattern)), negated=negated),
    )


RX = FieldLookup.REGEX
IRX = FieldLookup.IREGEX

CASES: list[tuple[str, QueryStatement, set[int]]] = [
    ('regex_is_case_sensitive', match(RX, r'^john'), {2, 3}),
    ('iregex_ignores_case', match(IRX, r'^JOHN'), {1, 2, 3}),
    ('iregex_ignores_case_outside_ascii', match(IRX, r'^шЛЮЗ$'), {4}),
    ('regex_leading_inline_ignorecase', match(RX, r'(?i)^john$'), {1}),
    ('escaped_metacharacters_are_literal', match(RX, r'C\.S\.A'), {5}),
    ('quote_in_pattern', match(RX, "it's"), {5}),
]

# A whole word "john", written in each engine's own syntax: it works on that database only.
POSTGRES_SYNTAX_CASE = ('postgres_word_boundary', match(IRX, r'\yjohn\y'), {1, 2})
PYTHON_RE_SYNTAX_CASE = ('python_re_word_boundary', match(IRX, r'\bjohn\b'), {1, 2})
