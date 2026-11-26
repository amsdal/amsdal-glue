"""Shared dataset and cases for `regex` / `iregex` on a text column, run by the SQLite and PostgreSQL suites.

The pattern is a Python `re` string passed to the database unchanged. On SQLite, the connection's `REGEXP`
function runs it with Python `re`; PostgreSQL runs it with its own engine (`~` / `~*`). A pattern written
with the portable forms gives the same rows on both. Where the engines differ, the case pins both answers,
so the documented differences (docs/regex-lookups.md) cannot go stale.

Each case is ``(case_id, QueryStatement, expected ids on PostgreSQL, expected ids on SQLite)``.
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
NBSP = '\u00a0'

ROWS: list[dict[str, Any]] = [
    {'id': 1, 'text': 'Emil'},
    {'id': 2, 'text': 'emil smith'},
    {'id': 3, 'text': 'loan receipt'},
    {'id': 4, 'text': f'loan{NBSP}receipt'},
    {'id': 5, 'text': 'a\nb'},
    {'id': 6, 'text': 'abc\n'},
    {'id': 7, 'text': '\u0663'},  # ARABIC-INDIC DIGIT THREE
    {'id': 8, 'text': 'Οδος'},
    {'id': 9, 'text': 'aba'},
    {'id': 10, 'text': 'AB'},
    {'id': 11, 'text': 'aa'},
    {'id': 12, 'text': "it's C.S.A"},
    {'id': 13, 'text': 'CxSxA'},
    {'id': 14, 'text': None},
    {'id': 15, 'text': 'axb'},
    {'id': 16, 'text': 'abc'},
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

PORTABLE_CASES: list[tuple[str, QueryStatement, set[int], set[int]]] = [
    ('regex_is_case_sensitive', match(RX, r'^emil'), {2}, {2}),
    ('iregex_ignores_case', match(IRX, r'^EMIL'), {1, 2}, {1, 2}),
    ('regex_leading_inline_ignorecase', match(RX, r'(?i)^emil$'), {1}, {1}),
    ('iregex_with_leading_inline_ignorecase', match(IRX, r'(?i)^EMIL$'), {1}, {1}),
    ('escaped_metacharacters_are_literal', match(RX, r'C\.S\.A'), {12}, {12}),
    ('quote_in_pattern', match(RX, "it's"), {12}, {12}),
    ('word_boundary_as_lookaround', match(IRX, r'(?<!\w)emil(?!\w)'), {1, 2}, {1, 2}),
    ('whitespace_class_with_nbsp', match(RX, r'^loan[\s\u00a0\u2007\u202f]+receipt$'), {3, 4}, {3, 4}),
    ('any_but_newline_as_class', match(RX, r'^a[^\n]b$'), {15}, {15}),
    ('very_end_of_string', match(RX, r'^abc\Z'), {16}, {16}),
    ('ascii_digit_class', match(RX, r'^[0-9]$'), set(), set()),
]

# One case per difference documented in docs/regex-lookups.md: (PostgreSQL, SQLite).
DIFFERENCE_CASES: list[tuple[str, QueryStatement, set[int], set[int]]] = [
    ('whitespace_shorthand_and_nbsp', match(RX, r'^loan\s+receipt$'), {3}, {3, 4}),
    ('digit_shorthand_and_non_ascii_digit', match(RX, r'^\d$'), set(), {7}),
    ('dot_and_newline', match(RX, r'^a.b$'), {5, 15}, {15}),
    ('dollar_before_final_newline', match(RX, r'^abc$'), {16}, {6, 16}),
    ('backslash_b_is_backspace_on_postgres', match(IRX, r'\bemil\b'), set(), {1, 2}),
    ('final_sigma_case_mapping', match(IRX, r'^οδοσ$'), set(), {8}),
    ('backreference_inside_repetition', match(RX, r'^(?:(a)|b)*\1$'), {11}, {9, 11}),
    ('brace_without_lower_bound', match(RX, r'^a{,3}$'), set(), {11}),
    ('two_digit_hex_escape', match(RX, r'^\x41B$'), set(), {10}),
    # PostgreSQL-only syntax. glibc also counts the Arabic-Indic digit (row 7) as `alpha`. Python `re` reads
    # `[[:alpha:]]+` as the set `[:alph` followed by `]+`, so nothing matches.
    ('postgres_posix_class', match(RX, r'^[[:alpha:]]+$'), {1, 7, 8, 9, 10, 11, 13, 15, 16}, set()),
]

CASES = PORTABLE_CASES + DIFFERENCE_CASES
