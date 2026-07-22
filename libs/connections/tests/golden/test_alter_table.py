# libs/connections/tests/golden/test_alter_table.py
"""Tests for ALTER / DROP / RENAME DDL paths.

Covers: AddProperty, DeleteProperty, RenameProperty, UpdateProperty,
AddConstraint, DeleteConstraint, AddIndex, DeleteIndex,
DeleteSchema (DROP TABLE), RenameSchema (RENAME TABLE) -
for both SQLite and Postgres dialects where feasible.

Generator-vs-driver rule (SQLite unsupported mutations)
--------------------------------------------------------
The SqlGenerator raises ``UnsupportedFeatureError`` directly for
SQLite mutations it cannot compile without a live connection:
- AddConstraint (all constraint types)
- DeleteConstraint
- UpdateProperty (ALTER COLUMN TYPE not supported in SQLite)
These are asserted with ``pytest.raises(UnsupportedFeatureError)``.

The multi-statement table-rebuild path for these mutations lives in the
SQLite connection driver (tested in sqlite integration), NOT here.
"""

import pytest
from amsdal_glue_connections._sql_core import UnsupportedFeatureError
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
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.types import DecimalType
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import ScalarType
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
        schema_ref=_ref(),
        property=PropertySchema(name='email', type=ScalarType.TEXT, required=False),
    )
    assert lite_ddl(m) == [('ALTER TABLE "Person" ADD COLUMN "email" text', [])]


def test_add_property_pg() -> None:
    m = AddProperty(
        schema_ref=_ref(),
        property=PropertySchema(name='email', type=ScalarType.TEXT, required=False),
    )
    assert pg_ddl(m) == [('ALTER TABLE "Person" ADD COLUMN "email" text', [])]


# ===========================================================================
# DeleteProperty
# ===========================================================================


def test_delete_property_sqlite() -> None:
    m = DeleteProperty(schema_ref=_ref(), property_name='email')
    assert lite_ddl(m) == [('ALTER TABLE "Person" DROP COLUMN "email"', [])]


def test_delete_property_pg() -> None:
    m = DeleteProperty(schema_ref=_ref(), property_name='email')
    assert pg_ddl(m) == [('ALTER TABLE "Person" DROP COLUMN "email"', [])]


# ===========================================================================
# RenameProperty
# ===========================================================================


def test_rename_property_sqlite() -> None:
    m = RenameProperty(schema_ref=_ref(), old_name='email', new_name='email_address')
    assert lite_ddl(m) == [
        ('ALTER TABLE "Person" RENAME COLUMN "email" TO "email_address"', []),
    ]


def test_rename_property_pg() -> None:
    m = RenameProperty(schema_ref=_ref(), old_name='email', new_name='email_address')
    assert pg_ddl(m) == [
        ('ALTER TABLE "Person" RENAME COLUMN "email" TO "email_address"', []),
    ]


# ===========================================================================
# UpdateProperty
# ===========================================================================


def test_update_property_sqlite() -> None:
    """SQLite UpdateProperty: the generator raises UnsupportedFeatureError.

    The multi-statement column-type rebuild lives in the SQLite connection
    driver (tested in sqlite integration), not in the SQL generator.
    """
    m = UpdateProperty(
        schema_ref=_ref(),
        property=PropertySchema(name='email', type=ScalarType.TEXT, required=False),
    )
    with pytest.raises(UnsupportedFeatureError):
        lite_ddl(m)


def test_update_property_pg() -> None:
    m = UpdateProperty(
        schema_ref=_ref(),
        property=PropertySchema(name='email', type=ScalarType.TEXT, required=False),
    )
    # The generator emits three separate ALTER TABLE statements:
    # SET DATA TYPE, DROP NOT NULL, DROP DEFAULT.
    # text is a non-numeric target: no USING cast (PG has an assignment cast).
    assert pg_ddl(m) == [
        ('ALTER TABLE "Person" ALTER COLUMN "email" SET DATA TYPE text', []),
        ('ALTER TABLE "Person" ALTER COLUMN "email" DROP NOT NULL', []),
        ('ALTER TABLE "Person" ALTER COLUMN "email" DROP DEFAULT', []),
    ]


def test_update_property_pg_double_target_has_using_cast() -> None:
    # Number field -> double precision (post-remap FLOAT->DOUBLE) must add USING:
    # PG cannot auto-cast text->double precision without an explicit USING clause.
    m = UpdateProperty(
        schema_ref=_ref(),
        property=PropertySchema(name='amount', type=ScalarType.DOUBLE, required=False),
    )
    assert pg_ddl(m)[0] == (
        'ALTER TABLE "Person" ALTER COLUMN "amount" SET DATA TYPE double precision '
        'USING "amount"::double precision',
        [],
    )


def test_update_property_pg_bigint_target_has_using_cast() -> None:
    m = UpdateProperty(
        schema_ref=_ref(),
        property=PropertySchema(name='counter', type=ScalarType.BIGINT, required=False),
    )
    assert pg_ddl(m)[0] == (
        'ALTER TABLE "Person" ALTER COLUMN "counter" SET DATA TYPE bigint '
        'USING "counter"::bigint',
        [],
    )


def test_update_property_pg_decimal_target_has_using_cast() -> None:
    m = UpdateProperty(
        schema_ref=_ref(),
        property=PropertySchema(name='price', type=DecimalType(precision=10, scale=2), required=False),
    )
    assert pg_ddl(m)[0] == (
        'ALTER TABLE "Person" ALTER COLUMN "price" SET DATA TYPE NUMERIC(10, 2) '
        'USING "price"::NUMERIC(10, 2)',
        [],
    )


def test_update_property_pg_non_numeric_target_has_no_using() -> None:
    # text target: no USING clause is emitted.
    m = UpdateProperty(
        schema_ref=_ref(),
        property=PropertySchema(name='email', type=ScalarType.TEXT, required=False),
    )
    first_sql = pg_ddl(m)[0][0]
    assert first_sql == 'ALTER TABLE "Person" ALTER COLUMN "email" SET DATA TYPE text'
    assert 'USING' not in first_sql


# ===========================================================================
# AddConstraint
# ===========================================================================


def test_add_constraint_sqlite() -> None:
    """SQLite AddConstraint: the generator raises UnsupportedFeatureError.

    The table-rebuild path lives in the SQLite connection driver
    (tested in sqlite integration), not in the SQL generator.
    """
    m = AddConstraint(
        schema_ref=_ref(),
        constraint=UniqueConstraint(name='uq_person_email', fields=['email']),
    )
    with pytest.raises(UnsupportedFeatureError):
        lite_ddl(m)


def test_add_constraint_pg() -> None:
    m = AddConstraint(
        schema_ref=_ref(),
        constraint=UniqueConstraint(name='uq_person_email', fields=['email']),
    )
    assert pg_ddl(m) == [
        ('ALTER TABLE "Person" ADD CONSTRAINT "uq_person_email" UNIQUE ("email")', []),
    ]


def test_add_constraint_pg_unique_quoted_correct_behaviour() -> None:
    # All constraint names are quoted.
    m = AddConstraint(
        schema_ref=_ref(),
        constraint=UniqueConstraint(name='uq_person_email', fields=['email']),
    )
    captured = pg_ddl(m)
    sql = captured[0][0]
    assert 'ADD CONSTRAINT "uq_person_email" UNIQUE ("email")' in sql
    assert 'ADD CONSTRAINT uq_person_email' not in sql


def test_add_constraint_pg_primary_key() -> None:
    m = AddConstraint(
        schema_ref=_ref(),
        constraint=PrimaryKeyConstraint(name='pk_person', fields=['id']),
    )
    assert pg_ddl(m) == [
        ('ALTER TABLE "Person" ADD CONSTRAINT "pk_person" PRIMARY KEY ("id")', []),
    ]


def test_add_constraint_pg_primary_key_quoted_correct_behaviour() -> None:
    # All constraint names are quoted.
    m = AddConstraint(
        schema_ref=_ref(),
        constraint=PrimaryKeyConstraint(name='pk_person', fields=['id']),
    )
    captured = pg_ddl(m)
    sql = captured[0][0]
    assert 'ADD CONSTRAINT "pk_person" PRIMARY KEY ("id")' in sql
    assert 'ADD CONSTRAINT pk_person' not in sql


def test_add_constraint_pg_foreign_key() -> None:
    m = AddConstraint(
        schema_ref=_ref(),
        constraint=ForeignKeyConstraint(
            name='fk_person_address',
            fields=['address_id'],
            reference_schema=SchemaReference(name='Address', version=Version.LATEST),
            reference_fields=['id'],
        ),
    )
    assert pg_ddl(m) == [
        (
            'ALTER TABLE "Person" ADD CONSTRAINT "fk_person_address" FOREIGN KEY ("address_id") REFERENCES "Address" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION',  # noqa: E501
            [],
        ),
    ]


def test_add_constraint_pg_check() -> None:
    m = AddConstraint(
        schema_ref=_ref(),
        constraint=CheckConstraint(
            name='chk_age_positive',
            condition=_gt_condition('Person', 'age', 0),
        ),
    )
    assert pg_ddl(m) == [
        ('ALTER TABLE "Person" ADD CONSTRAINT "chk_age_positive" CHECK ("Person"."age" > 0)', []),
    ]


def test_add_constraint_pg_check_quoted_correct_behaviour() -> None:
    # All constraint names are quoted.
    m = AddConstraint(
        schema_ref=_ref(),
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


def test_delete_constraint_sqlite() -> None:
    """SQLite DeleteConstraint: the generator raises UnsupportedFeatureError.

    The table-rebuild path lives in the SQLite connection driver
    (tested in sqlite integration), not in the SQL generator.
    """
    m = DeleteConstraint(schema_ref=_ref(), constraint_name='uq_person_email')
    with pytest.raises(UnsupportedFeatureError):
        lite_ddl(m)


def test_delete_constraint_pg() -> None:
    m = DeleteConstraint(schema_ref=_ref(), constraint_name='uq_person_email')
    assert pg_ddl(m) == [
        ('ALTER TABLE "Person" DROP CONSTRAINT "uq_person_email"', []),
    ]


# ===========================================================================
# AddIndex
# ===========================================================================


def test_add_index_sqlite() -> None:
    m = AddIndex(
        schema_ref=_ref(),
        index=IndexSchema(name='idx_person_email', fields=[IndexField(name='email')]),
    )
    assert lite_ddl(m) == [
        ('CREATE INDEX "idx_person_email" ON "Person" ("email" ASC)', []),
    ]


def test_add_index_pg() -> None:
    m = AddIndex(
        schema_ref=_ref(),
        index=IndexSchema(name='idx_person_email', fields=[IndexField(name='email')]),
    )
    assert pg_ddl(m) == [
        ('CREATE INDEX "idx_person_email" ON "Person" USING btree ("email" ASC)', []),
    ]


# ===========================================================================
# DeleteIndex
# ===========================================================================


def test_delete_index_sqlite() -> None:
    m = DeleteIndex(schema_ref=_ref(), index_name='idx_person_email')
    assert lite_ddl(m) == [('DROP INDEX "idx_person_email"', [])]


def test_delete_index_pg() -> None:
    m = DeleteIndex(schema_ref=_ref(), index_name='idx_person_email')
    assert pg_ddl(m) == [('DROP INDEX "idx_person_email"', [])]


# ===========================================================================
# DeleteSchema  (DROP TABLE)
# ===========================================================================


def test_drop_table_sqlite() -> None:
    m = DeleteSchema(schema_ref=_ref())
    assert lite_ddl(m) == [('DROP TABLE "Person"', [])]


def test_drop_table_pg() -> None:
    m = DeleteSchema(schema_ref=_ref())
    assert pg_ddl(m) == [('DROP TABLE "Person"', [])]


# ===========================================================================
# RenameSchema  (RENAME TABLE)
# ===========================================================================


def test_rename_table_sqlite() -> None:
    m = RenameSchema(schema_ref=_ref(), new_name='People')
    assert lite_ddl(m) == [('ALTER TABLE "Person" RENAME TO "People"', [])]


def test_rename_table_pg() -> None:
    m = RenameSchema(schema_ref=_ref(), new_name='People')
    assert pg_ddl(m) == [('ALTER TABLE "Person" RENAME TO "People"', [])]
