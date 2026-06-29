from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.limit import LimitQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version

from ._harness import lite
from ._harness import pg


def _ref(name: str) -> FieldReference:
    return FieldReference(field=Field(name=name), table_name='users')


# ---------------------------------------------------------------------------
# ORDER BY ASC
# ---------------------------------------------------------------------------


def test_order_by_asc_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        order_by=[OrderByQuery(field=_ref('name'), direction=OrderDirection.ASC)],
    )
    assert pg(q) == ('SELECT * FROM "users" ORDER BY "users"."name" ASC', [])


def test_order_by_asc_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        order_by=[OrderByQuery(field=_ref('name'), direction=OrderDirection.ASC)],
    )
    assert lite(q) == ("SELECT * FROM 'users' ORDER BY 'users'.'name' ASC", [])


# ---------------------------------------------------------------------------
# ORDER BY DESC
# ---------------------------------------------------------------------------


def test_order_by_desc_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        order_by=[OrderByQuery(field=_ref('created_at'), direction=OrderDirection.DESC)],
    )
    assert pg(q) == ('SELECT * FROM "users" ORDER BY "users"."created_at" DESC', [])


def test_order_by_desc_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        order_by=[OrderByQuery(field=_ref('created_at'), direction=OrderDirection.DESC)],
    )
    assert lite(q) == ("SELECT * FROM 'users' ORDER BY 'users'.'created_at' DESC", [])


# ---------------------------------------------------------------------------
# ORDER BY multiple fields
# ---------------------------------------------------------------------------


def test_order_by_multi_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        order_by=[
            OrderByQuery(field=_ref('name'), direction=OrderDirection.ASC),
            OrderByQuery(field=_ref('created_at'), direction=OrderDirection.DESC),
        ],
    )
    assert pg(q) == ('SELECT * FROM "users" ORDER BY "users"."name" ASC, "users"."created_at" DESC', [])


def test_order_by_multi_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        order_by=[
            OrderByQuery(field=_ref('name'), direction=OrderDirection.ASC),
            OrderByQuery(field=_ref('created_at'), direction=OrderDirection.DESC),
        ],
    )
    assert lite(q) == ("SELECT * FROM 'users' ORDER BY 'users'.'name' ASC, 'users'.'created_at' DESC", [])


# ---------------------------------------------------------------------------
# LIMIT only
# ---------------------------------------------------------------------------


def test_limit_only_pg() -> None:
    q = QueryStatement(table=SchemaReference(name='users', version=Version.LATEST), limit=LimitQuery(limit=10))
    assert pg(q) == ('SELECT * FROM "users" LIMIT 10', [])


def test_limit_only_sqlite() -> None:
    q = QueryStatement(table=SchemaReference(name='users', version=Version.LATEST), limit=LimitQuery(limit=10))
    assert lite(q) == ("SELECT * FROM 'users' LIMIT 10", [])


# ---------------------------------------------------------------------------
# LIMIT + OFFSET
# ---------------------------------------------------------------------------


def test_limit_offset_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        limit=LimitQuery(limit=10, offset=20),
    )
    assert pg(q) == ('SELECT * FROM "users" LIMIT 10 OFFSET 20', [])


def test_limit_offset_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        limit=LimitQuery(limit=10, offset=20),
    )
    assert lite(q) == ("SELECT * FROM 'users' LIMIT 10 OFFSET 20", [])
