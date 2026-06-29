# libs/connections/tests/golden/test_alter_table.py
"""Golden-master tests for ALTER / DROP / RENAME DDL paths.

Covers: AddProperty, DeleteProperty, RenameProperty, UpdateProperty,
AddConstraint, DeleteConstraint, AddIndex, DeleteIndex,
DeleteSchema (DROP TABLE), RenameSchema (RENAME TABLE) -
for both SQLite and Postgres dialects where feasible.

Introspection-bound mutations (SQLite AddConstraint / DeleteConstraint)
-----------------------------------------------------------------------
The SQLite implementation of AddConstraint and DeleteConstraint delegates to
``_recreate_table_with_constraints``, which immediately calls
``self.connection.execute('BEGIN')`` against the raw sqlite3.Connection object
(not through the overridable ``execute()`` hook).  Because the recording
harness never establishes a live DB connection, ``self.connection`` raises
``ConnectionError('Connection not established')`` before any SQL is built.
These tests are therefore marked ``xfail(strict=True)``.

SQLite UpdateProperty UUID non-determinism
------------------------------------------
The SQLite UpdateProperty path generates a temporary column name using
``uuid.uuid4().hex``, making exact SQL matching impossible.  The test
verifies the structural shape (4 statements, correct prefixes/suffixes)
instead of an exact byte-for-byte match.
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
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.schema import AddConstraint
from amsdal_glue_core.common.operations.mutations.schema import AddIndex
from amsdal_glue_core.common.operations.mutations.schema import AddProperty
from amsdal_glue_core.common.operations.mutations.schema import DeleteConstraint
from amsdal_glue_core.common.operations.mutations.schema import DeleteIndex
from amsdal_glue_core.common.operations.mutations.schema import DeleteProperty
from amsdal_glue_core.common.operations.mutations.schema import DeleteSchema
from amsdal_glue_core.common.operations.mutations.schema import RenameProperty
from amsdal_glue_core.common.operations.mutations.schema import RenameSchema
from amsdal_glue_core.common.operations.mutations.schema import UpdateProperty

from ._harness import lite_ddl
from ._harness import pg_ddl

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _ref() -> SchemaReference:
    return SchemaReference(name='Person', version=Version.LATEST)


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


# ===========================================================================
# AddProperty
# ===========================================================================


def test_add_property_sqlite() -> None:
    m = AddProperty(
        schema_reference=_ref(),
        property=PropertySchema(name='email', type=str, required=False),
    )
    assert lite_ddl(m) == [("ALTER TABLE 'Person' ADD COLUMN 'email' TEXT", [])]


def test_add_property_pg() -> None:
    m = AddProperty(
        schema_reference=_ref(),
        property=PropertySchema(name='email', type=str, required=False),
    )
    assert pg_ddl(m) == [('ALTER TABLE "Person" ADD COLUMN "email" TEXT', [])]


# ===========================================================================
# DeleteProperty
# ===========================================================================


def test_delete_property_sqlite() -> None:
    m = DeleteProperty(schema_reference=_ref(), property_name='email')
    assert lite_ddl(m) == [("ALTER TABLE 'Person' DROP COLUMN 'email'", [])]


def test_delete_property_pg() -> None:
    m = DeleteProperty(schema_reference=_ref(), property_name='email')
    assert pg_ddl(m) == [('ALTER TABLE "Person" DROP COLUMN "email"', [])]


# ===========================================================================
# RenameProperty
# ===========================================================================


def test_rename_property_sqlite() -> None:
    m = RenameProperty(schema_reference=_ref(), old_name='email', new_name='email_address')
    assert lite_ddl(m) == [
        ("ALTER TABLE 'Person' RENAME COLUMN 'email' TO 'email_address'", []),
    ]


def test_rename_property_pg() -> None:
    m = RenameProperty(schema_reference=_ref(), old_name='email', new_name='email_address')
    assert pg_ddl(m) == [
        ('ALTER TABLE "Person" RENAME COLUMN "email" TO "email_address"', []),
    ]


# ===========================================================================
# UpdateProperty
# ===========================================================================


def test_update_property_sqlite() -> None:
    """SQLite UpdateProperty: 4-step column-type migration.

    The temp column name is generated with ``uuid.uuid4().hex`` so its exact
    value is non-deterministic.  We verify the structural shape instead of
    an exact byte-for-byte match.
    """
    m = UpdateProperty(
        schema_reference=_ref(),
        property=PropertySchema(name='email', type=str, required=False),
    )
    result = lite_ddl(m)
    assert len(result) == 4
    sql0, p0 = result[0]
    sql1, p1 = result[1]
    sql2, p2 = result[2]
    sql3, p3 = result[3]
    # All have empty params
    assert p0 == p1 == p2 == p3 == []
    # Step 0: ADD temp UUID column (starts with 'f' + 32 hex chars)
    assert sql0.startswith("ALTER TABLE 'Person' ADD COLUMN 'f")
    assert sql0.endswith("' TEXT")
    # Step 1: UPDATE (copy data from original to temp)
    assert sql1.startswith("UPDATE 'Person' SET 'f")
    assert sql1.endswith("' = 'Person'.'email'")
    # Step 2: DROP original column (fully deterministic)
    assert sql2 == "ALTER TABLE 'Person' DROP COLUMN 'email'"
    # Step 3: RENAME temp -> original
    assert sql3.startswith("ALTER TABLE 'Person' RENAME COLUMN 'f")
    assert sql3.endswith("' TO 'email'")


def test_update_property_pg() -> None:
    m = UpdateProperty(
        schema_reference=_ref(),
        property=PropertySchema(name='email', type=str, required=False),
    )
    # KNOWN-DIVERGENCE (migration): PG UPDATE COLUMN emits ALTER COLUMN TYPE + DROP NOT NULL
    # as a comma-separated sequence within a single ALTER TABLE statement.
    assert pg_ddl(m) == [
        (
            'ALTER TABLE "Person" ALTER COLUMN "email" TYPE TEXT, ALTER COLUMN "email" DROP NOT NULL',
            [],
        ),
    ]


# ===========================================================================
# AddConstraint
# ===========================================================================


@pytest.mark.xfail(
    strict=True,
    reason='requires live-DB schema introspection; covered by corpus/integration Tasks 16-18',
)
def test_add_constraint_sqlite() -> None:
    """SQLite AddConstraint re-creates the table via _recreate_table_with_constraints,
    which calls self.connection.execute('BEGIN') on the raw sqlite3.Connection.
    The recording harness never establishes a connection -> ConnectionError."""
    m = AddConstraint(
        schema_reference=_ref(),
        constraint=UniqueConstraint(name='uq_person_email', fields=['email']),
    )
    lite_ddl(m)


def test_add_constraint_pg() -> None:
    m = AddConstraint(
        schema_reference=_ref(),
        constraint=UniqueConstraint(name='uq_person_email', fields=['email']),
    )
    # KNOWN-DIVERGENCE (migration): PG _build_constraint for UniqueConstraint does
    # NOT quote the constraint name.  Current output:
    # `CONSTRAINT uq_person_email UNIQUE ("email")` (unquoted constraint name).
    # Correct PG: `CONSTRAINT "uq_person_email" UNIQUE ("email")`.  FK constraint
    # names ARE quoted in PG (see test_create_table.py), making this an internal
    # inconsistency.  The Rust generator is expected to fix this.
    assert pg_ddl(m) == [
        ('ALTER TABLE "Person" ADD CONSTRAINT uq_person_email UNIQUE ("email")', []),
    ]


@pytest.mark.xfail(strict=True, reason='correct behaviour — to be fixed by qcraft/Rust migration; see §3-D7')
def test_add_constraint_pg_unique_quoted_correct_behaviour() -> None:
    m = AddConstraint(
        schema_reference=_ref(),
        constraint=UniqueConstraint(name='uq_person_email', fields=['email']),
    )
    captured = pg_ddl(m)
    sql = captured[0][0]
    assert 'ADD CONSTRAINT "uq_person_email" UNIQUE ("email")' in sql
    assert 'ADD CONSTRAINT uq_person_email' not in sql


def test_add_constraint_pg_primary_key() -> None:
    m = AddConstraint(
        schema_reference=_ref(),
        constraint=PrimaryKeyConstraint(name='pk_person', fields=['id']),
    )
    # KNOWN-DIVERGENCE (migration): PG _build_constraint for PrimaryKeyConstraint does
    # NOT quote the constraint name and appends a trailing space.  Current output:
    # `CONSTRAINT pk_person PRIMARY KEY ("id") ` (unquoted name, trailing space).
    # Correct PG: `CONSTRAINT "pk_person" PRIMARY KEY ("id")` (quoted name, no trailing space).
    # FK constraint names ARE quoted in PG (see test_add_constraint_pg_foreign_key),
    # making this an internal inconsistency.  The Rust generator is expected to fix this.
    assert pg_ddl(m) == [
        ('ALTER TABLE "Person" ADD CONSTRAINT pk_person PRIMARY KEY ("id") ', []),
    ]


@pytest.mark.xfail(strict=True, reason='correct behaviour — to be fixed by qcraft/Rust migration; see §3-D12')
def test_add_constraint_pg_primary_key_quoted_correct_behaviour() -> None:
    m = AddConstraint(
        schema_reference=_ref(),
        constraint=PrimaryKeyConstraint(name='pk_person', fields=['id']),
    )
    captured = pg_ddl(m)
    sql = captured[0][0]
    assert 'ADD CONSTRAINT "pk_person" PRIMARY KEY ("id")' in sql
    assert 'ADD CONSTRAINT pk_person' not in sql


def test_add_constraint_pg_foreign_key() -> None:
    m = AddConstraint(
        schema_reference=_ref(),
        constraint=ForeignKeyConstraint(
            name='fk_person_address',
            fields=['address_id'],
            reference_schema=SchemaReference(name='Address', version=Version.LATEST),
            reference_fields=['id'],
        ),
    )
    # FK constraint names are correctly quoted in PG — clean characterization, no divergence.
    assert pg_ddl(m) == [
        (
            'ALTER TABLE "Person" ADD CONSTRAINT "fk_person_address"'
            ' FOREIGN KEY ("address_id") REFERENCES "Address" ("id")',
            [],
        ),
    ]


def test_add_constraint_pg_check() -> None:
    m = AddConstraint(
        schema_reference=_ref(),
        constraint=CheckConstraint(
            name='chk_age_positive',
            condition=_gt_condition('Person', 'age', 0),
        ),
    )
    # KNOWN-DIVERGENCE (migration): PG _build_constraint for CheckConstraint does
    # NOT quote the constraint name.  Current output:
    # `CONSTRAINT chk_age_positive CHECK ("Person"."age" > 0)` (unquoted name).
    # Correct PG: `CONSTRAINT "chk_age_positive" CHECK ("Person"."age" > 0)`.
    # FK constraint names ARE quoted in PG (see test_add_constraint_pg_foreign_key),
    # making this an internal inconsistency.  The Rust generator is expected to fix this.
    assert pg_ddl(m) == [
        ('ALTER TABLE "Person" ADD CONSTRAINT chk_age_positive CHECK ("Person"."age" > 0)', []),
    ]


@pytest.mark.xfail(strict=True, reason='correct behaviour — to be fixed by qcraft/Rust migration; see §3-D13')
def test_add_constraint_pg_check_quoted_correct_behaviour() -> None:
    m = AddConstraint(
        schema_reference=_ref(),
        constraint=CheckConstraint(
            name='chk_age_positive',
            condition=_gt_condition('Person', 'age', 0),
        ),
    )
    captured = pg_ddl(m)
    sql = captured[0][0]
    assert 'ADD CONSTRAINT "chk_age_positive" CHECK ("Person"."age" > 0)' in sql
    assert 'ADD CONSTRAINT chk_age_positive' not in sql


# ===========================================================================
# DeleteConstraint
# ===========================================================================


@pytest.mark.xfail(
    strict=True,
    reason='requires live-DB schema introspection; covered by corpus/integration Tasks 16-18',
)
def test_delete_constraint_sqlite() -> None:
    """SQLite DeleteConstraint re-creates the table via _recreate_table_with_constraints,
    which calls self.connection.execute('BEGIN') on the raw sqlite3.Connection.
    The recording harness never establishes a connection -> ConnectionError."""
    m = DeleteConstraint(schema_reference=_ref(), constraint_name='uq_person_email')
    lite_ddl(m)


def test_delete_constraint_pg() -> None:
    m = DeleteConstraint(schema_reference=_ref(), constraint_name='uq_person_email')
    assert pg_ddl(m) == [
        ('ALTER TABLE "Person" DROP CONSTRAINT "uq_person_email"', []),
    ]


# ===========================================================================
# AddIndex
# ===========================================================================


def test_add_index_sqlite() -> None:
    m = AddIndex(
        schema_reference=_ref(),
        index=IndexSchema(name='idx_person_email', fields=['email']),
    )
    assert lite_ddl(m) == [
        ("CREATE INDEX 'idx_person_email' ON 'Person' ('email')", []),
    ]


def test_add_index_pg() -> None:
    m = AddIndex(
        schema_reference=_ref(),
        index=IndexSchema(name='idx_person_email', fields=['email']),
    )
    assert pg_ddl(m) == [
        ('CREATE INDEX "idx_person_email" ON "Person" ("email")', []),
    ]


# ===========================================================================
# DeleteIndex
# ===========================================================================


def test_delete_index_sqlite() -> None:
    m = DeleteIndex(schema_reference=_ref(), index_name='idx_person_email')
    assert lite_ddl(m) == [("DROP INDEX 'idx_person_email'", [])]


def test_delete_index_pg() -> None:
    m = DeleteIndex(schema_reference=_ref(), index_name='idx_person_email')
    assert pg_ddl(m) == [('DROP INDEX "idx_person_email"', [])]


# ===========================================================================
# DeleteSchema  (DROP TABLE)
# ===========================================================================


def test_drop_table_sqlite() -> None:
    m = DeleteSchema(schema_reference=_ref())
    assert lite_ddl(m) == [("DROP TABLE 'Person'", [])]


def test_drop_table_pg() -> None:
    m = DeleteSchema(schema_reference=_ref())
    assert pg_ddl(m) == [('DROP TABLE "Person"', [])]


# ===========================================================================
# RenameSchema  (RENAME TABLE)
# ===========================================================================


def test_rename_table_sqlite() -> None:
    m = RenameSchema(schema_reference=_ref(), new_schema_name='People')
    assert lite_ddl(m) == [("ALTER TABLE 'Person' RENAME TO 'People'", [])]


def test_rename_table_pg() -> None:
    m = RenameSchema(schema_reference=_ref(), new_schema_name='People')
    assert pg_ddl(m) == [('ALTER TABLE "Person" RENAME TO "People"', [])]
