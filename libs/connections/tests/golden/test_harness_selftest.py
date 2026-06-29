from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version

from ._harness import lite
from ._harness import pg


def test_pg_simple_select() -> None:
    q = QueryStatement(table=SchemaReference(name='users', version=Version.LATEST))
    assert pg(q) == ('SELECT * FROM "users"', [])


def test_sqlite_simple_select() -> None:
    q = QueryStatement(table=SchemaReference(name='users', version=Version.LATEST))
    sql, params = lite(q)
    assert sql.startswith('SELECT * FROM ')
    assert params == []
