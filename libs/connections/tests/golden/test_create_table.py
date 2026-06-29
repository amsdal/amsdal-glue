# libs/connections/tests/golden/test_create_table.py
"""Golden-master tests for CREATE TABLE DDL paths.

Covers: CREATE TABLE with columns + defaults, PRIMARY KEY, UNIQUE,
FOREIGN KEY, CHECK constraints, and CREATE INDEX — for both SQLite
and Postgres dialects.

SQLite uses the build_schema_mutation / schema_builder.py code path
(single-quoted identifiers). Postgres drives _create_table() inline
on the connection class (double-quoted identifiers).

Note on SQLite AddConstraint / DeleteConstraint
------------------------------------------------
These two mutation types are intentionally absent from this golden file.
Their SQLite implementation in ``_run_schema_mutation`` delegates to
``_recreate_table_with_constraints``, which immediately calls
``self.connection.execute('BEGIN')`` and ``query_schema()`` — both of
which require a live database connection.  Because this golden-file
harness generates SQL without connecting to any DB, capturing those
paths here is out of scope.  They are covered by the corpus/integration
capture instead (Tasks 16-18).
"""

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.schema import AddIndex
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from ._harness import lite_ddl
from ._harness import pg_ddl

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _gt_condition(table: str, field: str, value: object) -> Conditions:
    """Return a Conditions wrapping a single field > value check."""
    return Conditions(
        Condition(
            left=FieldReferenceExpression(
                field_reference=FieldReference(field=Field(name=field), table_name=table),
            ),
            lookup=FieldLookup.GT,
            right=Value(value=value),
        )
    )


# ---------------------------------------------------------------------------
# PRIMARY KEY + column defaults + CREATE INDEX
# ---------------------------------------------------------------------------


def test_register_schema_sqlite() -> None:
    stmts = lite_ddl(
        RegisterSchema(
            schema=Schema(
                name='Person',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=int, required=True),
                    PropertySchema(name='name', type=str, required=True),
                    PropertySchema(name='age', type=int, required=False, default=18),
                ],
                constraints=[PrimaryKeyConstraint(name='pk_person', fields=['id'])],
                indexes=[IndexSchema(name='idx_person_name', fields=['name'])],
            ),
        ),
    )
    assert stmts == [
        (
            "CREATE TABLE 'Person' ("
            "'id' INTEGER NOT NULL, "
            "'name' TEXT NOT NULL, "
            "'age' INTEGER DEFAULT 18, "
            "CONSTRAINT 'pk_person' PRIMARY KEY ('id')"
            ')',
            [],
        ),
        ("CREATE INDEX 'idx_person_name' ON 'Person' ('name')", []),
    ]


def test_register_schema_pg() -> None:
    stmts = pg_ddl(
        RegisterSchema(
            schema=Schema(
                name='Person',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=int, required=True),
                    PropertySchema(name='name', type=str, required=True),
                    PropertySchema(name='age', type=int, required=False, default=18),
                ],
                constraints=[PrimaryKeyConstraint(name='pk_person', fields=['id'])],
                indexes=[IndexSchema(name='idx_person_name', fields=['name'])],
            ),
        ),
    )
    # KNOWN-DIVERGENCE (migration): PG _build_constraint for PrimaryKeyConstraint
    # does NOT quote the constraint name and appends a trailing space before the
    # closing paren.  Current output: `CONSTRAINT pk_person PRIMARY KEY ("id") `
    # (unquoted name + trailing space before `)`) .  Correct PG:
    # `CONSTRAINT "pk_person" PRIMARY KEY ("id")`.  Note: FK constraint names
    # ARE quoted in PG (see test_foreign_key_constraint_pg), making this an
    # internal inconsistency.  The Rust generator is expected to fix this: quote
    # all constraint names and drop the trailing space.
    assert stmts == [
        (
            'CREATE TABLE "Person" ('
            '"id" BIGINT NOT NULL, '
            '"name" TEXT NOT NULL, '
            '"age" BIGINT DEFAULT 18, '
            'CONSTRAINT pk_person PRIMARY KEY ("id") '
            ')',
            [],
        ),
        ('CREATE INDEX "idx_person_name" ON "Person" ("name")', []),
    ]


# ---------------------------------------------------------------------------
# UNIQUE constraint
# ---------------------------------------------------------------------------


def test_unique_constraint_sqlite() -> None:
    stmts = lite_ddl(
        RegisterSchema(
            schema=Schema(
                name='Person',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=int, required=True),
                    PropertySchema(name='email', type=str, required=True),
                ],
                constraints=[UniqueConstraint(name='uq_person_email', fields=['email'])],
            ),
        ),
    )
    assert stmts == [
        (
            "CREATE TABLE 'Person' ("
            "'id' INTEGER NOT NULL, "
            "'email' TEXT NOT NULL, "
            "CONSTRAINT 'uq_person_email' UNIQUE ('email')"
            ')',
            [],
        ),
    ]


def test_unique_constraint_pg() -> None:
    stmts = pg_ddl(
        RegisterSchema(
            schema=Schema(
                name='Person',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=int, required=True),
                    PropertySchema(name='email', type=str, required=True),
                ],
                constraints=[UniqueConstraint(name='uq_person_email', fields=['email'])],
            ),
        ),
    )
    # KNOWN-DIVERGENCE (migration): PG _build_constraint for UniqueConstraint does
    # NOT quote the constraint name.  Current output:
    # `CONSTRAINT uq_person_email UNIQUE ("email")` (unquoted name).
    # Correct PG: `CONSTRAINT "uq_person_email" UNIQUE ("email")`.  Note: FK
    # constraint names ARE quoted in PG (see test_foreign_key_constraint_pg),
    # making this an internal inconsistency.  The Rust generator is expected to
    # fix this: quote all constraint names.
    assert stmts == [
        (
            'CREATE TABLE "Person" ('
            '"id" BIGINT NOT NULL, '
            '"email" TEXT NOT NULL, '
            'CONSTRAINT uq_person_email UNIQUE ("email")'
            ')',
            [],
        ),
    ]


# ---------------------------------------------------------------------------
# FOREIGN KEY constraint
# ---------------------------------------------------------------------------


def test_foreign_key_constraint_sqlite() -> None:
    stmts = lite_ddl(
        RegisterSchema(
            schema=Schema(
                name='Order',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=int, required=True),
                    PropertySchema(name='person_id', type=int, required=True),
                ],
                constraints=[
                    ForeignKeyConstraint(
                        name='fk_order_person',
                        fields=['person_id'],
                        reference_schema=SchemaReference(name='Person', version=Version.LATEST),
                        reference_fields=['id'],
                    )
                ],
            ),
        ),
    )
    # KNOWN-DIVERGENCE (migration): SQLite build_constraint does not quote
    # reference_fields — produces `(id)` instead of the correct `('id')`.
    assert stmts == [
        (
            "CREATE TABLE 'Order' ("
            "'id' INTEGER NOT NULL, "
            "'person_id' INTEGER NOT NULL, "
            "CONSTRAINT 'fk_order_person' FOREIGN KEY ('person_id') REFERENCES 'Person' (id)"
            ')',
            [],
        ),
    ]


def test_foreign_key_constraint_pg() -> None:
    stmts = pg_ddl(
        RegisterSchema(
            schema=Schema(
                name='Order',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=int, required=True),
                    PropertySchema(name='person_id', type=int, required=True),
                ],
                constraints=[
                    ForeignKeyConstraint(
                        name='fk_order_person',
                        fields=['person_id'],
                        reference_schema=SchemaReference(name='Person', version=Version.LATEST),
                        reference_fields=['id'],
                    )
                ],
            ),
        ),
    )
    # Note: PG _build_constraint for ForeignKeyConstraint DOES quote the constraint
    # name (unlike PrimaryKey/Unique which do not) — intentional per base.py.
    assert stmts == [
        (
            'CREATE TABLE "Order" ('
            '"id" BIGINT NOT NULL, '
            '"person_id" BIGINT NOT NULL, '
            'CONSTRAINT "fk_order_person" FOREIGN KEY ("person_id") REFERENCES "Person" ("id")'
            ')',
            [],
        ),
    ]


# ---------------------------------------------------------------------------
# CHECK constraint
# ---------------------------------------------------------------------------


def test_check_constraint_sqlite() -> None:
    stmts = lite_ddl(
        RegisterSchema(
            schema=Schema(
                name='Person',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=int, required=True),
                    PropertySchema(name='age', type=int, required=True),
                ],
                constraints=[
                    CheckConstraint(
                        name='chk_age_positive',
                        condition=_gt_condition('Person', 'age', 0),
                    )
                ],
            ),
        ),
    )
    # build_where with embed_values=True renders table-qualified field names
    # using the SQLite transform (single quotes).
    assert stmts == [
        (
            "CREATE TABLE 'Person' ("
            "'id' INTEGER NOT NULL, "
            "'age' INTEGER NOT NULL, "
            "CONSTRAINT 'chk_age_positive' CHECK ('Person'.'age' > 0)"
            ')',
            [],
        ),
    ]


def test_check_constraint_pg() -> None:
    stmts = pg_ddl(
        RegisterSchema(
            schema=Schema(
                name='Person',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=int, required=True),
                    PropertySchema(name='age', type=int, required=True),
                ],
                constraints=[
                    CheckConstraint(
                        name='chk_age_positive',
                        condition=_gt_condition('Person', 'age', 0),
                    )
                ],
            ),
        ),
    )
    # KNOWN-DIVERGENCE (migration): PG uses double-quoted identifiers but the
    # constraint name is NOT quoted.  Current output:
    # `CONSTRAINT chk_age_positive CHECK ("Person"."age" > 0)` (unquoted name).
    # Correct PG: `CONSTRAINT "chk_age_positive" CHECK ("Person"."age" > 0)`.
    # Note: FK constraint names ARE quoted in PG (see
    # test_foreign_key_constraint_pg), making this an internal inconsistency.
    # The Rust generator is expected to fix this: quote all constraint names.
    assert stmts == [
        (
            'CREATE TABLE "Person" ('
            '"id" BIGINT NOT NULL, '
            '"age" BIGINT NOT NULL, '
            'CONSTRAINT chk_age_positive CHECK ("Person"."age" > 0)'
            ')',
            [],
        ),
    ]


# ---------------------------------------------------------------------------
# Standalone CREATE INDEX (AddIndex mutation)
# ---------------------------------------------------------------------------


def test_add_index_sqlite() -> None:
    stmts = lite_ddl(
        AddIndex(
            schema_reference=SchemaReference(name='Person', version=Version.LATEST),
            index=IndexSchema(name='idx_person_email', fields=['email']),
        ),
    )
    assert stmts == [
        ("CREATE INDEX 'idx_person_email' ON 'Person' ('email')", []),
    ]


def test_add_index_pg() -> None:
    stmts = pg_ddl(
        AddIndex(
            schema_reference=SchemaReference(name='Person', version=Version.LATEST),
            index=IndexSchema(name='idx_person_email', fields=['email']),
        ),
    )
    assert stmts == [
        ('CREATE INDEX "idx_person_email" ON "Person" ("email")', []),
    ]
