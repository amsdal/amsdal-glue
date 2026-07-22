"""Introspection regression tests for the SQLite review fixes.

- CHECK / partial-index predicates that the extended parser now understands (``IS [NOT] NULL``,
  ``LIKE``) must reconstruct into proper conditions, and a predicate it still cannot represent
  (``IN`` with a nested paren the DDL regex cannot capture) must degrade to ``condition=None``
  rather than aborting the whole ``query_schema`` (previously a hard ``ValueError``).
- A ``WITHOUT ROWID`` table's secondary index must report only its real key columns, not the
  auxiliary PK columns the ``pragma_index_xinfo`` view also exposes.
"""

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.func import Func
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY


def _get_schema(connection: SqliteConnection, table_name: str) -> Schema:
    query = QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
    schemas = [schema for schema in connection.query_schema(query) if schema.name == table_name]
    assert schemas, f'schema {table_name!r} not found'
    return schemas[0]


def _field_ref(name: str) -> FieldReferenceExpression:
    return FieldReferenceExpression(field_reference=FieldReference(field=Field(name=name), table_name=''))


def test_partial_index_is_not_null_reconstructed(database_connection: SqliteConnection) -> None:
    database_connection.execute('CREATE TABLE "users" ("id" INTEGER PRIMARY KEY, "email" TEXT)')
    database_connection.execute('CREATE INDEX "idx_has_email" ON "users" ("id") WHERE "email" IS NOT NULL')

    schema = _get_schema(database_connection, 'users')
    idx = next(i for i in (schema.indexes or []) if i.name == 'idx_has_email')

    assert idx.condition == Conditions(
        Condition(left=_field_ref('email'), lookup=FieldLookup.ISNULL, right=Value(value=False))
    )


def test_check_with_like_reconstructed(database_connection: SqliteConnection) -> None:
    database_connection.execute(
        'CREATE TABLE "people" ('
        '"id" INTEGER PRIMARY KEY, '
        '"email" TEXT NOT NULL, '
        'CONSTRAINT "chk_email" CHECK (email LIKE \'%@%\')'
        ')'
    )

    schema = _get_schema(database_connection, 'people')
    checks = [c for c in (schema.constraints or []) if isinstance(c, CheckConstraint)]

    assert checks == [
        CheckConstraint(
            name='chk_email',
            condition=Conditions(
                Condition(left=_field_ref('email'), lookup=FieldLookup.CONTAINS, right=Value(value='@'))
            ),
        )
    ]


def test_check_with_unrepresentable_predicate_degrades_without_crash(database_connection: SqliteConnection) -> None:
    # The DDL regex cannot capture the nested paren of an IN-list, so the predicate is unparseable;
    # introspection must still succeed with ``condition=None`` rather than aborting the schema.
    database_connection.execute(
        'CREATE TABLE "flagged" ('
        '"id" INTEGER PRIMARY KEY, '
        '"status" TEXT NOT NULL, '
        "CONSTRAINT \"chk_status\" CHECK (status IN ('a', 'b'))"
        ')'
    )

    schema = _get_schema(database_connection, 'flagged')
    checks = [c for c in (schema.constraints or []) if isinstance(c, CheckConstraint)]

    assert len(checks) == 1
    assert checks[0].name == 'chk_status'
    assert checks[0].condition is None


def test_without_rowid_index_reports_only_key_columns(database_connection: SqliteConnection) -> None:
    database_connection.execute('CREATE TABLE "wr" ("a" INTEGER, "b" INTEGER, PRIMARY KEY("a")) WITHOUT ROWID')
    database_connection.execute('CREATE INDEX "idx_b" ON "wr" ("b")')

    schema = _get_schema(database_connection, 'wr')
    idx = next(i for i in (schema.indexes or []) if i.name == 'idx_b')

    # Only the real key column ``b`` -- not the auxiliary PK column ``a`` that pragma_index_xinfo
    # also lists for a WITHOUT ROWID table.
    assert idx.fields == [IndexField(name='b', direction=OrderDirection.ASC)]


def test_generated_not_expression_reconstructed(database_connection: SqliteConnection) -> None:
    # A GENERATED column using unary NOT must reconstruct as a proper Func node, not a RawExpression
    # embedding the repr() of an Expression (which would be invalid SQL).
    database_connection.execute(
        'CREATE TABLE "toggles" ('
        '"id" INTEGER PRIMARY KEY, '
        '"active" INTEGER NOT NULL, '
        '"inactive" INTEGER GENERATED ALWAYS AS (NOT "active") STORED'
        ')'
    )

    schema = _get_schema(database_connection, 'toggles')
    inactive = next(p for p in schema.properties if p.name == 'inactive')

    assert inactive.generated == Func(name='NOT', args=[_field_ref('active')])
