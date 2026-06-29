from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version

from ._harness import lite
from ._harness import pg
from ._harness import pg_ddl


def test_pg_simple_select() -> None:
    q = QueryStatement(table=SchemaReference(name='users', version=Version.LATEST))
    assert pg(q) == ('SELECT * FROM "users"', [])


def test_sqlite_simple_select() -> None:
    q = QueryStatement(table=SchemaReference(name='users', version=Version.LATEST))
    sql, params = lite(q)
    assert sql.startswith('SELECT * FROM ')
    assert params == []


def test_pg_ddl_uses_double_quoted_identifiers() -> None:
    """Proves pg_ddl characterises the REAL Postgres inline DDL path (double quotes),
    not build_schema_mutation (single quotes)."""
    from amsdal_glue_core.common.data_models.schema import PropertySchema
    from amsdal_glue_core.common.data_models.schema import Schema
    from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

    stmts = pg_ddl(
        RegisterSchema(
            schema=Schema(
                name='users',
                version=Version.LATEST,
                properties=[PropertySchema(name='id', type=int, required=True)],
            ),
        ),
    )
    # At least one statement, and the CREATE TABLE uses double-quoted identifiers.
    create = next(sql for sql, _ in stmts if sql.startswith('CREATE TABLE'))
    assert '"users"' in create
    assert "'users'" not in create
