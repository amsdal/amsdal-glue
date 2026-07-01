from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.mutations.data import InsertData

from ._harness import lite_cmd
from ._harness import pg_cmd


def test_insert_single_sqlite() -> None:
    m = InsertData(
        schema=SchemaReference(name='users', version=Version.LATEST),
        data=[Data(data={'id': 1, 'name': 'Alice'})],
    )
    # Re-baselined: SQLite now uses ANSI double-quoted identifiers — DIFFERENT-BUT-VALID
    assert lite_cmd(m) == ('INSERT INTO "users" ("id", "name") VALUES (?, ?)', [1, 'Alice'])


def test_insert_multi_sqlite() -> None:
    m = InsertData(
        schema=SchemaReference(name='users', version=Version.LATEST),
        data=[Data(data={'id': 1, 'name': 'Alice'}), Data(data={'id': 2, 'name': 'Bob'})],
    )
    # Re-baselined: SQLite now uses ANSI double-quoted identifiers — DIFFERENT-BUT-VALID
    assert lite_cmd(m) == ('INSERT INTO "users" ("id", "name") VALUES (?, ?), (?, ?)', [1, 'Alice', 2, 'Bob'])


def test_insert_single_pg() -> None:
    m = InsertData(
        schema=SchemaReference(name='users', version=Version.LATEST),
        data=[Data(data={'id': 1, 'name': 'Alice'})],
    )
    assert pg_cmd(m) == ('INSERT INTO "users" ("id", "name") VALUES (%s, %s)', [1, 'Alice'])


def test_insert_multi_pg() -> None:
    m = InsertData(
        schema=SchemaReference(name='users', version=Version.LATEST),
        data=[Data(data={'id': 1, 'name': 'Alice'}), Data(data={'id': 2, 'name': 'Bob'})],
    )
    assert pg_cmd(m) == ('INSERT INTO "users" ("id", "name") VALUES (%s, %s), (%s, %s)', [1, 'Alice', 2, 'Bob'])
