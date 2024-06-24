# mypy: disable-error-code="type-abstract"
import sqlite3
import tempfile
from collections.abc import Generator

import pytest
from amsdal_glue.initialize import init_default_containers
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_core.commands.planner.data_command_planner import DataCommandPlanner
from amsdal_glue_core.commands.planner.lock_command_planner import LockCommandPlanner
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.metadata import Metadata
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import LockAction
from amsdal_glue_core.common.enums import LockMode
from amsdal_glue_core.common.enums import LockParameter
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.helpers.singleton import Singleton
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.commands import LockCommand
from amsdal_glue_core.common.operations.commands import LockSchemaReference
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.services.managers.connection import ConnectionManager
from amsdal_glue_core.containers import Container


@pytest.fixture(autouse=True)
def _register_default_connection() -> Generator[None, None, None]:
    init_default_containers()
    connection_mng = Container.managers.get(ConnectionManager)

    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = f'{temp_dir}/data.sqlite'

        shipping_connection = SqliteConnection()
        customers_connection = SqliteConnection()
        connection_mng.register_connection(shipping_connection, schema_name='shippings')
        connection_mng.register_connection(customers_connection, schema_name='customers')

        shipping_connection.connect(db_path=db_path, check_same_thread=False)
        customers_connection.connect(db_path=db_path, check_same_thread=False)
        shipping_connection.execute('CREATE TABLE IF NOT EXISTS shippings (id TEXT, customer_id TEXT, status TEXT)')
        customers_connection.execute('CREATE TABLE IF NOT EXISTS customers (id TEXT, name TEXT)')

        yield

        shipping_connection.execute('DROP TABLE shippings')
        customers_connection.execute('DROP TABLE customers')
        shipping_connection.disconnect()
        customers_connection.disconnect()

    Singleton.invalidate_all_instances()


def test_lock() -> None:
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
    lock_plan.execute()

    query = DataCommand(
        lock_id=None,
        transaction_id=None,
        mutations=[
            InsertData(
                schema=SchemaReference(name='shippings', version=Version.LATEST),
                data=[
                    Data(
                        data={'id': '111', 'customer_id': '1', 'status': 'shipped'},
                        metadata=Metadata(
                            object_id='1',
                            object_version='1',
                            created_at='2021-01-01T00:00:00Z',
                            updated_at='2021-01-01T00:00:00Z',
                        ),
                    )
                ],
            )
        ],
    )
    planner = Container.planners.get(DataCommandPlanner)
    plan = planner.plan_data_command(query)

    try:
        plan.execute()
    except ConnectionError as e:
        assert 'Error executing mutation:' in str(e)
        assert str(e.__cause__.__cause__) == 'database is locked'  # type: ignore[union-attr]
        assert isinstance(e.__cause__.__cause__, sqlite3.OperationalError)  # type: ignore[union-attr]

    else:
        msg = 'Expected ConnectionError'
        raise AssertionError(msg)

    with pytest.raises(ConnectionError):
        (
            ConnectionManager()  # type: ignore[attr-defined]
            .get_connection('shippings')
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
    lock_plan.execute()

    plan.execute()
    assert (
        [('111', '1', 'shipped')]
        == ConnectionManager()  # type: ignore[attr-defined]
        .get_connection('shippings')
        .execute('SELECT id, customer_id, status FROM shippings')
        .fetchall()
    )
