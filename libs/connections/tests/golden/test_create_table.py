# libs/connections/tests/golden/test_create_table.py
"""Golden-master tests for CREATE TABLE DDL paths.

Covers: CREATE TABLE with columns + defaults, PRIMARY KEY, UNIQUE,
FOREIGN KEY, CHECK constraints, and CREATE INDEX — for both SQLite
and Postgres dialects.

Both SQLite and Postgres now route through the Rust SqlGenerator
(``compile_schema_mutation``), which uses ANSI double-quoted identifiers
for both dialects and lowercase type names.
"""

import pytest
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import ScalarType
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
            schema_ref=SchemaReference(name='Person', version=Version.LATEST),
            schema=Schema(
                name='Person',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                    PropertySchema(name='name', type=ScalarType.TEXT, required=True),
                    PropertySchema(name='age', type=ScalarType.INTEGER, required=False, default=Value(value=18)),
                ],
                constraints=[PrimaryKeyConstraint(name='pk_person', fields=['id'])],
                indexes=[IndexSchema(name='idx_person_name', fields=[IndexField(name='name')])],
            ),
        ),
    )
    assert stmts == [
        (
            'CREATE TABLE "Person" ('
            '"id" integer NOT NULL, '
            '"name" text NOT NULL, '
            '"age" integer DEFAULT (18), '
            'CONSTRAINT "pk_person" PRIMARY KEY ("id")'
            ')',
            [],
        ),
        ('CREATE INDEX "idx_person_name" ON "Person" ("name" ASC)', []),
    ]


def test_register_schema_pg() -> None:
    stmts = pg_ddl(
        RegisterSchema(
            schema_ref=SchemaReference(name='Person', version=Version.LATEST),
            schema=Schema(
                name='Person',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                    PropertySchema(name='name', type=ScalarType.TEXT, required=True),
                    PropertySchema(name='age', type=ScalarType.INTEGER, required=False, default=Value(value=18)),
                ],
                constraints=[PrimaryKeyConstraint(name='pk_person', fields=['id'])],
                indexes=[IndexSchema(name='idx_person_name', fields=[IndexField(name='name')])],
            ),
        ),
    )
    assert stmts == [
        (
            'CREATE TABLE "Person" ('
            '"id" integer NOT NULL, '
            '"name" text NOT NULL, '
            '"age" integer DEFAULT 18, '
            'CONSTRAINT "pk_person" PRIMARY KEY ("id")'
            ')',
            [],
        ),
        ('CREATE INDEX "idx_person_name" ON "Person" USING btree ("name" ASC)', []),
    ]


def test_register_schema_pg_pk_quoted_correct_behaviour() -> None:
    # Rust generator now correctly quotes all constraint names and emits no trailing
    # space — the divergence tracked by §3-D6 is resolved.
    captured = pg_ddl(
        RegisterSchema(
            schema_ref=SchemaReference(name='Person', version=Version.LATEST),
            schema=Schema(
                name='Person',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                    PropertySchema(name='name', type=ScalarType.TEXT, required=True),
                    PropertySchema(name='age', type=ScalarType.INTEGER, required=False, default=Value(value=18)),
                ],
                constraints=[PrimaryKeyConstraint(name='pk_person', fields=['id'])],
                indexes=[IndexSchema(name='idx_person_name', fields=[IndexField(name='name')])],
            ),
        ),
    )
    sql = captured[0][0]
    assert 'CONSTRAINT "pk_person" PRIMARY KEY ("id")' in sql
    assert 'CONSTRAINT pk_person' not in sql
    assert '("id") )' not in sql


# ---------------------------------------------------------------------------
# UNIQUE constraint
# ---------------------------------------------------------------------------


def test_unique_constraint_sqlite() -> None:
    stmts = lite_ddl(
        RegisterSchema(
            schema_ref=SchemaReference(name='Person', version=Version.LATEST),
            schema=Schema(
                name='Person',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                    PropertySchema(name='email', type=ScalarType.TEXT, required=True),
                ],
                constraints=[UniqueConstraint(name='uq_person_email', fields=['email'])],
            ),
        ),
    )
    assert stmts == [
        (
            'CREATE TABLE "Person" ('
            '"id" integer NOT NULL, '
            '"email" text NOT NULL, '
            'CONSTRAINT "uq_person_email" UNIQUE ("email")'
            ')',
            [],
        ),
    ]


def test_unique_constraint_pg() -> None:
    stmts = pg_ddl(
        RegisterSchema(
            schema_ref=SchemaReference(name='Person', version=Version.LATEST),
            schema=Schema(
                name='Person',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                    PropertySchema(name='email', type=ScalarType.TEXT, required=True),
                ],
                constraints=[UniqueConstraint(name='uq_person_email', fields=['email'])],
            ),
        ),
    )
    assert stmts == [
        (
            'CREATE TABLE "Person" ('
            '"id" integer NOT NULL, '
            '"email" text NOT NULL, '
            'CONSTRAINT "uq_person_email" UNIQUE ("email")'
            ')',
            [],
        ),
    ]


def test_unique_constraint_pg_quoted_correct_behaviour() -> None:
    # Rust generator now correctly quotes all constraint names — §3-D7 resolved.
    captured = pg_ddl(
        RegisterSchema(
            schema_ref=SchemaReference(name='Person', version=Version.LATEST),
            schema=Schema(
                name='Person',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                    PropertySchema(name='email', type=ScalarType.TEXT, required=True),
                ],
                constraints=[UniqueConstraint(name='uq_person_email', fields=['email'])],
            ),
        ),
    )
    sql = captured[0][0]
    assert 'CONSTRAINT "uq_person_email" UNIQUE ("email")' in sql
    assert 'CONSTRAINT uq_person_email' not in sql


# ---------------------------------------------------------------------------
# FOREIGN KEY constraint
# ---------------------------------------------------------------------------


def test_foreign_key_constraint_sqlite() -> None:
    stmts = lite_ddl(
        RegisterSchema(
            schema_ref=SchemaReference(name='Order', version=Version.LATEST),
            schema=Schema(
                name='Order',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                    PropertySchema(name='person_id', type=ScalarType.INTEGER, required=True),
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
    assert stmts == [
        (
            'CREATE TABLE "Order" ('
            '"id" integer NOT NULL, '
            '"person_id" integer NOT NULL, '
            'CONSTRAINT "fk_order_person" FOREIGN KEY ("person_id") REFERENCES "Person" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION'
            ')',
            [],
        ),
    ]


def test_foreign_key_sqlite_reference_fields_quoted_correct_behaviour() -> None:
    # D8: REFERENCES 'Person' should use ANSI double-quoted identifiers.
    stmts = lite_ddl(
        RegisterSchema(
            schema_ref=SchemaReference(name='Order', version=Version.LATEST),
            schema=Schema(
                name='Order',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                    PropertySchema(name='person_id', type=ScalarType.INTEGER, required=True),
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
    sql = stmts[0][0]
    assert 'REFERENCES "Person" ("id")' in sql
    assert "REFERENCES 'Person'" not in sql
    assert "REFERENCES Person" not in sql


def test_foreign_key_constraint_pg() -> None:
    stmts = pg_ddl(
        RegisterSchema(
            schema_ref=SchemaReference(name='Order', version=Version.LATEST),
            schema=Schema(
                name='Order',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                    PropertySchema(name='person_id', type=ScalarType.INTEGER, required=True),
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
    assert stmts == [
        (
            'CREATE TABLE "Order" ('
            '"id" integer NOT NULL, '
            '"person_id" integer NOT NULL, '
            'CONSTRAINT "fk_order_person" FOREIGN KEY ("person_id") REFERENCES "Person" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION'
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
            schema_ref=SchemaReference(name='Person', version=Version.LATEST),
            schema=Schema(
                name='Person',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                    PropertySchema(name='age', type=ScalarType.INTEGER, required=True),
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
    assert stmts == [
        (
            'CREATE TABLE "Person" ('
            '"id" integer NOT NULL, '
            '"age" integer NOT NULL, '
            'CONSTRAINT "chk_age_positive" CHECK ("Person"."age" > 0)'
            ')',
            [],
        ),
    ]


def test_check_constraint_pg() -> None:
    stmts = pg_ddl(
        RegisterSchema(
            schema_ref=SchemaReference(name='Person', version=Version.LATEST),
            schema=Schema(
                name='Person',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                    PropertySchema(name='age', type=ScalarType.INTEGER, required=True),
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
    assert stmts == [
        (
            'CREATE TABLE "Person" ('
            '"id" integer NOT NULL, '
            '"age" integer NOT NULL, '
            'CONSTRAINT "chk_age_positive" CHECK ("Person"."age" > 0)'
            ')',
            [],
        ),
    ]


def test_check_constraint_pg_quoted_correct_behaviour() -> None:
    # Rust generator now correctly quotes all constraint names — §3-D9 resolved.
    captured = pg_ddl(
        RegisterSchema(
            schema_ref=SchemaReference(name='Person', version=Version.LATEST),
            schema=Schema(
                name='Person',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                    PropertySchema(name='age', type=ScalarType.INTEGER, required=True),
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
    sql = captured[0][0]
    assert 'CONSTRAINT "chk_age_positive" CHECK ("Person"."age" > 0)' in sql
    assert 'CONSTRAINT chk_age_positive' not in sql


# ---------------------------------------------------------------------------
# Standalone CREATE INDEX (AddIndex mutation)
# ---------------------------------------------------------------------------


def test_add_index_sqlite() -> None:
    stmts = lite_ddl(
        AddIndex(
            schema_ref=SchemaReference(name='Person', version=Version.LATEST),
            index=IndexSchema(name='idx_person_email', fields=[IndexField(name='email')]),
        ),
    )
    assert stmts == [
        ('CREATE INDEX "idx_person_email" ON "Person" ("email" ASC)', []),
    ]


def test_add_index_pg() -> None:
    stmts = pg_ddl(
        AddIndex(
            schema_ref=SchemaReference(name='Person', version=Version.LATEST),
            index=IndexSchema(name='idx_person_email', fields=[IndexField(name='email')]),
        ),
    )
    assert stmts == [
        ('CREATE INDEX "idx_person_email" ON "Person" USING btree ("email" ASC)', []),
    ]
