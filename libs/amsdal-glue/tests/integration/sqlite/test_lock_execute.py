# mypy: disable-error-code="type-abstract"
import sqlite3
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_core.commands.planner.data_command_planner import DataCommandPlanner
from amsdal_glue_core.commands.planner.lock_command_planner import LockCommandPlanner
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import LockAction
from amsdal_glue_core.common.enums import LockMode
from amsdal_glue_core.common.enums import LockParameter
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.commands import LockCommand
from amsdal_glue_core.common.operations.commands import LockSchemaReference
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.containers import Container

from amsdal_glue.connections.connection_pool import DefaultConnectionPool
from amsdal_glue.initialize import init_default_containers


@pytest.fixture(autouse=True)
def _register_default_connection() -> Generator[None, None, None]:
    init_default_containers()
    connection_mng = Container.managers.get(ConnectionManager)

    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(f'{temp_dir}/data.sqlite')

        connection_mng.register_connection_pool(
            DefaultConnectionPool(SqliteConnection, db_path=db_path, check_same_thread=False, timeout=0.3),
            schema_name='shippings',
        )
        connection_mng.register_connection_pool(
            DefaultConnectionPool(SqliteConnection, db_path=db_path, check_same_thread=False, timeout=0.3),
            schema_name='customers',
        )

        connection_mng.get_connection_pool('shippings').get_connection().execute(  # type: ignore[attr-defined]
            'CREATE TABLE IF NOT EXISTS shippings (id TEXT, customer_id TEXT, status TEXT)'
        )
        connection_mng.get_connection_pool('customers').get_connection().execute(  # type: ignore[attr-defined]
            'CREATE TABLE IF NOT EXISTS customers (id TEXT, name TEXT)'
        )

        try:
            yield
        finally:
            connection_mng.disconnect_all()


def test_lock() -> None:
    connection_mng = Container.managers.get(ConnectionManager)
    lock_planner = Container.planners.get(LockCommandPlanner)
    lock_plan = lock_planner.plan_lock(
        LockCommand(
            lock_id=None,
            transaction_id=None,
            action=LockAction.ACQUIRE,
            mode=LockMode.EXCLUSIVE,
            parameter=LockParameter.SKIP_LOCKED,
            locked_objects=[LockSchemaReference(schema=SchemaReference(name='customers', version=Version.LATEST))],
        )
    )
    lock_plan.execute(transaction_id=None, lock_id=None)

    query = DataCommand(
        lock_id=None,
        transaction_id=None,
        mutations=[
            InsertData(
                schema=SchemaReference(name='shippings', version=Version.LATEST),
                data=[
                    Data(
                        data={'id': '111', 'customer_id': '1', 'status': 'shipped'},
                    )
                ],
            )
        ],
    )
    planner = Container.planners.get(DataCommandPlanner)
    plan = planner.plan_data_command(query)

    try:
        plan.execute(transaction_id=None, lock_id=None)
    except ConnectionError as e:
        assert 'Mutation failed: Error executing SQL:' in str(e)
        assert str(e.__cause__.__cause__) == 'database is locked'  # type: ignore[union-attr]
        assert isinstance(e.__cause__.__cause__, sqlite3.OperationalError)  # type: ignore[union-attr]

    else:
        msg = 'Expected ConnectionError'
        raise AssertionError(msg)

    with pytest.raises(ConnectionError):
        (
            connection_mng.get_connection_pool('shippings')  # type: ignore[attr-defined]
            .get_connection()
            .execute('SELECT id, customer_id, status FROM shippings')
            .fetchall()
        )

    lock_planner = Container.planners.get(LockCommandPlanner)
    lock_plan = lock_planner.plan_lock(
        LockCommand(
            lock_id=None,
            transaction_id=None,
            action=LockAction.RELEASE,
            mode=LockMode.EXCLUSIVE,
            parameter=LockParameter.SKIP_LOCKED,
            locked_objects=[LockSchemaReference(schema=SchemaReference(name='customers', version=Version.LATEST))],
        )
    )
    lock_plan.execute(transaction_id=None, lock_id=None)

    plan.execute(transaction_id=None, lock_id=None)
    assert (
        connection_mng.get_connection_pool('shippings')  # type: ignore[attr-defined]
        .get_connection()
        .execute('SELECT id, customer_id, status FROM shippings')
        .fetchall()
        == [('111', '1', 'shipped')]
    )
