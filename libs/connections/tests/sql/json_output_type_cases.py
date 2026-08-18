"""Shared dataset and case matrix for the ``output_type`` JSON semantics suite.

Postgres is the reference: every expected id set below is what Postgres returns for the query.
SQLite must return exactly the same set for the same ``QueryStatement``. Both dialect suites import
this module and assert against the SAME literal, so a bug shared by both engines cannot pass silently.

Fixture-free on purpose -- there is no ``tests/sql/conftest.py``, and each dialect's
``database_connection`` fixture lives in its own ``integration/conftest.py``.
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
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

TABLE = 'JsonOutputType'
SCALAR_TABLE = 'JsonScalarColumn'

# Row 6 carries a JSON ``null`` for ``age``; row 7 omits the ``age`` key entirely. Those two are
# different things in Postgres and must stay different in SQLite.
#
# The names are chosen so that no CONTAINS/STARTSWITH case can be satisfied by a different row under
# case-insensitive matching -- otherwise the test would be measuring SQLite's ASCII-case-insensitive
# LIKE (a known, out-of-scope engine difference) instead of the JSON extraction.
ROWS: list[dict[str, Any]] = [
    {'id': 1, 'payload': {'age': 5, 'name': 'Ann', 'active': False, 'score': 1.5, 'tags': ['x'], 'meta': {'k': 1}}},
    {
        'id': 2,
        'payload': {'age': 9, 'name': 'Bob', 'active': True, 'score': 10.0, 'tags': ['x', 'y'], 'meta': {'k': 2}},
    },
    {'id': 3, 'payload': {'age': 18, 'name': 'Emil', 'active': True, 'score': 2.25, 'tags': [], 'meta': {'k': 3}}},
    {'id': 4, 'payload': {'age': 36, 'name': 'Zoe', 'active': False, 'score': 99.0, 'tags': ['z'], 'meta': {'k': 4}}},
    {'id': 5, 'payload': {'age': 100, 'name': 'Mia', 'active': True, 'score': 0.5, 'tags': ['y'], 'meta': {'k': 5}}},
    {'id': 6, 'payload': {'age': None, 'active': True, 'score': 0.0, 'tags': [], 'meta': {'k': 6}}},
    {'id': 7, 'payload': {'name': 'Nik', 'active': True, 'score': 0.0, 'tags': [], 'meta': {'k': 7}}},
]

# A bare scalar cannot be JSON by construction the way a dict is, so its type has to be declared --
# which is exactly what `DataInput` makes possible. Before it, there was no way to say this at all:
# Postgres rejected the insert and SQLite silently stored invalid JSON.
SCALAR_ROWS: list[dict[str, Any]] = [
    {'id': 1, 'payload': Value('fr123ewew12', output_type=ScalarType.JSONB)},
    {'id': 2, 'payload': Value(1040, output_type=ScalarType.JSONB)},
]


def _schema(name: str) -> Schema:
    return Schema(
        name=name,
        version=Version.LATEST,
        properties=[
            PropertySchema(name='id', type=ScalarType.BIGINT, required=True),
            PropertySchema(name='payload', type=ScalarType.JSONB, required=False),
        ],
    )


def register_and_seed(database_connection: Any, name: str, rows: list[dict[str, Any]]) -> None:
    """Create the table and insert the rows THROUGH GLUE, so the insert path is covered too."""
    schema = _schema(name)
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema_ref=SchemaReference(name=name, version=Version.LATEST),
                    schema=schema,
                ),
            ],
        ),
    )
    database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name=name, version=Version.LATEST),
            data=[DataInput(data=dict(row)) for row in rows],
        ),
    ])


def ref(
    *path: str,
    output_type: ScalarType | None = None,
    table: str = TABLE,
) -> FieldReferenceExpression:
    """Build a (possibly nested) field reference: ``ref('payload', 'meta', 'k')`` -> ``payload__meta__k``."""
    field = Field(name=path[-1])
    for name in reversed(path[:-1]):
        field = Field(name=name, child=field)

    return FieldReferenceExpression(
        field_reference=FieldReference(field=field, table_name=table),
        output_type=output_type,
    )


def query(where: Conditions, table: str = TABLE) -> QueryStatement:
    return QueryStatement(table=SchemaReference(name=table, version=Version.LATEST), where=where)


def cond(left: Any, lookup: FieldLookup, right: Any) -> Conditions:
    return Conditions(Condition(left=left, lookup=lookup, right=right))


J = ScalarType.JSONB

# (case_id, QueryStatement, expected ids)
#
# Every expectation is the Postgres result. `age` is absent on row 7 and JSON-null on row 6, so any
# comparison on `age` excludes both -- in BOTH engines, which is exactly what is being pinned.
CASES: list[tuple[str, QueryStatement, set[int]]] = [
    # --- default (JSONB) extraction: compare the JSON value as JSON -------------------------------
    ('jsonb_age_gte_18', query(cond(ref('payload', 'age'), FieldLookup.GTE, Value(18, output_type=J))), {3, 4, 5}),
    ('jsonb_age_gt_9', query(cond(ref('payload', 'age'), FieldLookup.GT, Value(9, output_type=J))), {3, 4, 5}),
    # A JSON `null` is the LOWEST value in Postgres' jsonb ordering
    # (Object > Array > Boolean > Number > String > Null), so row 6 satisfies `< 18`, `<= 9` and
    # `!= 36`. Row 7, whose `age` key is ABSENT, yields SQL NULL and is excluded from all of them.
    ('jsonb_age_lt_18', query(cond(ref('payload', 'age'), FieldLookup.LT, Value(18, output_type=J))), {1, 2, 6}),
    ('jsonb_age_lte_9', query(cond(ref('payload', 'age'), FieldLookup.LTE, Value(9, output_type=J))), {1, 2, 6}),
    ('jsonb_age_eq_36', query(cond(ref('payload', 'age'), FieldLookup.EQ, Value(36, output_type=J))), {4}),
    (
        'jsonb_age_neq_36',
        query(cond(ref('payload', 'age'), FieldLookup.NEQ, Value(36, output_type=J))),
        {1, 2, 3, 5, 6},
    ),
    ('jsonb_age_in_18_36', query(cond(ref('payload', 'age'), FieldLookup.IN, Value([18, 36], output_type=J))), {3, 4}),
    # JSON null is a value, not SQL NULL -- it matches only row 6.
    ('jsonb_age_eq_json_null', query(cond(ref('payload', 'age'), FieldLookup.EQ, Value(None, output_type=J))), {6}),
    # A MISSING key is SQL NULL -- it matches only row 7. Row 6 (JSON null) must NOT match.
    ('jsonb_age_is_null_missing_key', query(cond(ref('payload', 'age'), FieldLookup.ISNULL, Value(value=True))), {7}),
    # Reversed operands: the Value sits on the left.
    (
        'jsonb_reversed_18_gt_age',
        query(cond(Value(18, output_type=J), FieldLookup.GT, ref('payload', 'age'))),
        {1, 2, 6},
    ),
    (
        'jsonb_score_gte_225',
        query(cond(ref('payload', 'score'), FieldLookup.GTE, Value(2.25, output_type=J))),
        {2, 3, 4},
    ),
    ('jsonb_name_eq_emil', query(cond(ref('payload', 'name'), FieldLookup.EQ, Value('Emil', output_type=J))), {3}),
    (
        'jsonb_active_eq_true',
        query(cond(ref('payload', 'active'), FieldLookup.EQ, Value(value=True, output_type=J))),
        {2, 3, 5, 6, 7},
    ),
    (
        'jsonb_active_eq_false',
        query(cond(ref('payload', 'active'), FieldLookup.EQ, Value(value=False, output_type=J))),
        {1, 4},
    ),
    # Two-level path.
    (
        'jsonb_meta_k_gte_4',
        query(cond(ref('payload', 'meta', 'k'), FieldLookup.GTE, Value(4, output_type=J))),
        {4, 5, 6, 7},
    ),
    # Container-valued nested fields: SQLite minifies its JSON output, Python json.dumps does not.
    ('jsonb_meta_eq_object', query(cond(ref('payload', 'meta'), FieldLookup.EQ, Value({'k': 3}, output_type=J))), {3}),
    ('jsonb_tags_eq_array', query(cond(ref('payload', 'tags'), FieldLookup.EQ, Value(['x', 'y'], output_type=J))), {2}),
    # --- TEXT extraction: Postgres' `->>` semantics, reproduced exactly ---------------------------
    # Text comparison IS lexicographic in Postgres: '5' >= '18' and '9' >= '18' are true, '100' is not.
    (
        'text_age_gte_18',
        query(cond(ref('payload', 'age', output_type=ScalarType.TEXT), FieldLookup.GTE, Value('18'))),
        {1, 2, 3, 4},
    ),
    (
        'text_age_lt_18',
        query(cond(ref('payload', 'age', output_type=ScalarType.TEXT), FieldLookup.LT, Value('18'))),
        {5},
    ),
    (
        'text_name_eq_emil',
        query(cond(ref('payload', 'name', output_type=ScalarType.TEXT), FieldLookup.EQ, Value('Emil'))),
        {3},
    ),
    (
        'text_name_contains_ob',
        query(cond(ref('payload', 'name', output_type=ScalarType.TEXT), FieldLookup.CONTAINS, Value('ob'))),
        {2},
    ),
    (
        'text_name_startswith_z',
        query(cond(ref('payload', 'name', output_type=ScalarType.TEXT), FieldLookup.STARTSWITH, Value('Z'))),
        {4},
    ),
    # A JSON boolean renders as the text 'true' in Postgres -- SQLite's `->>` gives INTEGER 1 instead.
    (
        'text_active_eq_true',
        query(cond(ref('payload', 'active', output_type=ScalarType.TEXT), FieldLookup.EQ, Value('true'))),
        {2, 3, 5, 6, 7},
    ),
    # --- typed extraction ------------------------------------------------------------------------
    (
        'bigint_age_gte_18',
        query(cond(ref('payload', 'age', output_type=ScalarType.BIGINT), FieldLookup.GTE, Value(18))),
        {3, 4, 5},
    ),
    (
        'bigint_age_lt_18',
        query(cond(ref('payload', 'age', output_type=ScalarType.BIGINT), FieldLookup.LT, Value(18))),
        {1, 2},
    ),
    (
        'numeric_score_gte_225',
        query(cond(ref('payload', 'score', output_type=ScalarType.NUMERIC), FieldLookup.GTE, Value(2.25))),
        {2, 3, 4},
    ),
    # --- whole JSON column -----------------------------------------------------------------------
    (
        'whole_column_eq_object',
        query(cond(ref('payload'), FieldLookup.EQ, Value(ROWS[2]['payload'], output_type=J))),
        {3},
    ),
    # --- whole JSON column text match -------------------------------------------------------------
    # The substring-over-serialized-JSON filters that amsdal_server emits for array/dict columns.
    # Postgres stores these columns as `jsonb`, which has no LIKE operator, so the left side must
    # carry a text cast or the query errors with `operator does not exist: jsonb ~~ unknown`.
    # Search terms stay inside one JSON token: the engines serialize whitespace differently, so a
    # pattern spanning a `,`/`:` separator is out of contract.
    ('whole_column_contains_emil', query(cond(ref('payload'), FieldLookup.CONTAINS, Value('Emil'))), {3}),
    ('whole_column_contains_wrong_case', query(cond(ref('payload'), FieldLookup.CONTAINS, Value('emil'))), set()),
    ('whole_column_icontains_emil', query(cond(ref('payload'), FieldLookup.ICONTAINS, Value('emil'))), {3}),
    ('whole_column_contains_tag_x', query(cond(ref('payload'), FieldLookup.CONTAINS, Value('x'))), {1, 2}),
    # --- nested field text match ------------------------------------------------------------------
    # A nested reference in a text match is the UNQUOTED `->>` text, not the quoted JSON
    # serialization -- otherwise STARTSWITH/ENDSWITH can never match the first/last character on
    # Postgres (`(payload->'name')::text` is `"Emil"`, quotes included) while SQLite's native
    # extraction matches, and the engines silently disagree. Row 6 has no `name` -> SQL NULL,
    # excluded everywhere.
    ('nested_name_startswith_E', query(cond(ref('payload', 'name'), FieldLookup.STARTSWITH, Value('E'))), {3}),
    ('nested_name_endswith_ob', query(cond(ref('payload', 'name'), FieldLookup.ENDSWITH, Value('ob'))), {2}),
    ('nested_name_contains_mi', query(cond(ref('payload', 'name'), FieldLookup.CONTAINS, Value('mi'))), {3}),
    ('nested_name_icontains_mi', query(cond(ref('payload', 'name'), FieldLookup.ICONTAINS, Value('mi'))), {3, 5}),
    ('nested_name_istartswith_z', query(cond(ref('payload', 'name'), FieldLookup.ISTARTSWITH, Value('z'))), {4}),
]

# Regex lookups executable on Postgres only: the SQLite connection registers no REGEXP function.
# Same jsonb-vs-text failure mode as LIKE: without a text cast (whole column) or a `->>` extraction
# (nested field), Postgres errors with `operator does not exist: jsonb ~ unknown`.
PG_REGEX_CASES: list[tuple[str, QueryStatement, set[int]]] = [
    ('regex_whole_column_emil', query(cond(ref('payload'), FieldLookup.REGEX, Value('Emil'))), {3}),
    ('regex_nested_name_anchored', query(cond(ref('payload', 'name'), FieldLookup.REGEX, Value('^Emil$'))), {3}),
    ('iregex_nested_name_anchored', query(cond(ref('payload', 'name'), FieldLookup.IREGEX, Value('^emil$'))), {3}),
]

# The case from the original report: a jsonb column holding a bare SCALAR.
SCALAR_CASES: list[tuple[str, QueryStatement, set[int]]] = [
    (
        'scalar_column_eq_str',
        query(
            cond(ref('payload', table=SCALAR_TABLE), FieldLookup.EQ, Value('fr123ewew12', output_type=J)),
            table=SCALAR_TABLE,
        ),
        {1},
    ),
    (
        'scalar_column_eq_int',
        query(cond(ref('payload', table=SCALAR_TABLE), FieldLookup.EQ, Value(1040, output_type=J)), table=SCALAR_TABLE),
        {2},
    ),
]
