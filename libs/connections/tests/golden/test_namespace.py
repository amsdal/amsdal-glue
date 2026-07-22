from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.data import DataInput
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.enums import ReferentialAction
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.data import DeleteData
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from ._harness import lite
from ._harness import lite_cmd
from ._harness import pg
from ._harness import pg_cmd
from ._harness import pg_ddl

# ---------------------------------------------------------------------------
# SELECT with namespace
# ---------------------------------------------------------------------------


def test_select_with_namespace_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST, namespace='public'),
    )
    assert pg(q) == ('SELECT * FROM "public"."users"', [])


def test_select_with_namespace_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST, namespace='mydb'),
    )
    assert lite(q) == ('SELECT * FROM "mydb"."users"', [])


def test_select_with_namespace_and_alias_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST, namespace='public', alias='u'),
    )
    assert pg(q) == ('SELECT * FROM "public"."users" AS "u"', [])


def test_select_columns_with_namespace_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST, namespace='public'),
        only=[
            FieldReference(field=Field(name='id'), table_name='users', namespace='public'),
            FieldReference(field=Field(name='name'), table_name='users', namespace='public'),
        ],
    )
    assert pg(q) == (
        'SELECT "public"."users"."id", "public"."users"."name" FROM "public"."users"',
        [],
    )


def test_field_ref_with_namespace_in_where_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST, namespace='public'),
        where=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(
                        field=Field(name='name'),
                        table_name='users',
                        namespace='public',
                    ),
                ),
                lookup=FieldLookup.EQ,
                right=Value('Alice'),
            ),
        ),
    )
    assert pg(q) == (
        'SELECT * FROM "public"."users" WHERE "public"."users"."name" = %s',
        ['Alice'],
    )


# ---------------------------------------------------------------------------
# JOIN with namespace
# ---------------------------------------------------------------------------


def test_join_with_namespace_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST, namespace='public'),
        joins=[
            JoinQuery(
                table=SchemaReference(name='orders', version=Version.LATEST, namespace='sales'),
                on=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(
                                field=Field(name='id'),
                                table_name='users',
                                namespace='public',
                            ),
                        ),
                        lookup=FieldLookup.EQ,
                        right=FieldReferenceExpression(
                            field_reference=FieldReference(
                                field=Field(name='user_id'),
                                table_name='orders',
                                namespace='sales',
                            ),
                        ),
                    ),
                ),
                join_type=JoinType.INNER,
            ),
        ],
    )
    assert pg(q) == (
        'SELECT "users".* FROM "public"."users"'
        ' INNER JOIN "sales"."orders"'
        ' ON "public"."users"."id" = "sales"."orders"."user_id"',
        [],
    )


# ---------------------------------------------------------------------------
# INSERT with namespace
# ---------------------------------------------------------------------------


def test_insert_with_namespace_pg() -> None:
    m = InsertData(
        schema=SchemaReference(name='users', version=Version.LATEST, namespace='public'),
        data=[DataInput(data={'name': 'Alice', 'age': 30})],
    )
    assert pg_cmd(m) == ('INSERT INTO "public"."users" ("name", "age") VALUES (%s, %s)', ['Alice', 30])


def test_insert_with_namespace_sqlite() -> None:
    m = InsertData(
        schema=SchemaReference(name='users', version=Version.LATEST, namespace='mydb'),
        data=[DataInput(data={'name': 'Alice', 'age': 30})],
    )
    assert lite_cmd(m) == ('INSERT INTO "mydb"."users" ("name", "age") VALUES (?, ?)', ['Alice', 30])


# ---------------------------------------------------------------------------
# UPDATE with namespace
# ---------------------------------------------------------------------------


def test_update_with_namespace_pg() -> None:
    m = UpdateData(
        schema=SchemaReference(name='users', version=Version.LATEST, namespace='public'),
        data=DataInput(data={'name': Value('Bob')}),
        query=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(
                        field=Field(name='id'),
                        table_name='users',
                        namespace='public',
                    ),
                ),
                lookup=FieldLookup.EQ,
                right=Value(1),
            ),
        ),
    )
    assert pg_cmd(m) == (
        'UPDATE "public"."users" SET "name" = %s WHERE "public"."users"."id" = %s',
        ['Bob', 1],
    )


# ---------------------------------------------------------------------------
# DELETE with namespace
# ---------------------------------------------------------------------------


def test_delete_with_namespace_pg() -> None:
    m = DeleteData(
        schema=SchemaReference(name='users', version=Version.LATEST, namespace='public'),
        query=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(
                        field=Field(name='id'),
                        table_name='users',
                        namespace='public',
                    ),
                ),
                lookup=FieldLookup.EQ,
                right=Value(1),
            ),
        ),
    )
    assert pg_cmd(m) == (
        'DELETE FROM "public"."users" WHERE "public"."users"."id" = %s',
        [1],
    )


# ---------------------------------------------------------------------------
# CREATE TABLE with namespace
# ---------------------------------------------------------------------------


def test_create_table_with_namespace_pg() -> None:
    m = RegisterSchema(
        schema_ref=SchemaReference(name='users', version=Version.LATEST, namespace='public'),
        schema=Schema(
            name='users',
            version=Version.LATEST,
            namespace='public',
            properties=[
                PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                PropertySchema(name='name', type=ScalarType.TEXT, required=True),
            ],
            constraints=[
                PrimaryKeyConstraint(name='pk_users', fields=['id']),
            ],
        ),
    )
    [(sql, params)] = pg_ddl(m)
    assert sql == (
        'CREATE TABLE "public"."users"'
        ' ("id" integer NOT NULL, "name" text NOT NULL,'
        ' CONSTRAINT "pk_users" PRIMARY KEY ("id"))'
    )
    assert params == []


# ---------------------------------------------------------------------------
# FK cross-namespace
# ---------------------------------------------------------------------------


def test_fk_cross_namespace_pg() -> None:
    m = RegisterSchema(
        schema_ref=SchemaReference(name='orders', version=Version.LATEST, namespace='sales'),
        schema=Schema(
            name='orders',
            version=Version.LATEST,
            namespace='sales',
            properties=[
                PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                PropertySchema(name='user_id', type=ScalarType.INTEGER, required=True),
            ],
            constraints=[
                PrimaryKeyConstraint(name='pk_orders', fields=['id']),
                ForeignKeyConstraint(
                    name='fk_orders_user',
                    fields=['user_id'],
                    reference_schema=SchemaReference(
                        name='users',
                        version=Version.LATEST,
                        namespace='public',
                    ),
                    reference_fields=['id'],
                    on_delete=ReferentialAction.CASCADE,
                    on_update=ReferentialAction.NO_ACTION,
                ),
            ],
        ),
    )
    [(sql, params)] = pg_ddl(m)
    assert 'CREATE TABLE "sales"."orders"' in sql
    assert 'REFERENCES "public"."users"' in sql
    assert params == []
