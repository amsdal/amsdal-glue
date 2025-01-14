# mypy: disable-error-code="type-abstract"
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_core.commands.planner.data_command_planner import DataCommandPlanner
from amsdal_glue_core.commands.planner.transaction_command_planner import TransactionCommandPlanner
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import TransactionAction
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.commands import TransactionCommand
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
        connection_pool = DefaultConnectionPool(SqliteConnection, db_path=db_path, check_same_thread=False, timeout=0.3)
        connection_mng.register_connection_pool(
            connection_pool,
            schema_name='shippings',
        )
        connection_mng.register_connection_pool(
            connection_pool,
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


def test_transaction() -> None:
    transaction_planner = Container.planners.get(TransactionCommandPlanner)
    command_planner = Container.planners.get(DataCommandPlanner)
    connection_mng = Container.managers.get(ConnectionManager)

    transaction_planner.plan_transaction(
        TransactionCommand(
            transaction_id='transaction_id',
            schema=SchemaReference(name='shippings', version=Version.LATEST),
            action=TransactionAction.BEGIN,
        )
    ).execute(transaction_id='transaction_id', lock_id=None)

    command_planner.plan_data_command(
        DataCommand(
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
                ),
                InsertData(
                    schema=SchemaReference(name='customers', version=Version.LATEST),
                    data=[
                        Data(
                            data={'id': '1', 'name': 'customer'},
                        )
                    ],
                ),
            ],
        )
    ).execute(transaction_id='transaction_id', lock_id=None)

    transaction_planner.plan_transaction(
        TransactionCommand(
            transaction_id='transaction_id',
            schema=SchemaReference(name='shippings', version=Version.LATEST),
            action=TransactionAction.COMMIT,
        )
    ).execute(transaction_id='transaction_id', lock_id=None)

    assert (
        connection_mng.get_connection_pool('shippings')  # type: ignore[attr-defined]
        .get_connection()
        .execute('SELECT id, customer_id, status FROM shippings')
        .fetchall()
        == [('111', '1', 'shipped')]
    )
    assert (
        connection_mng.get_connection_pool('customers')  # type: ignore[attr-defined]
        .get_connection()
        .execute('SELECT id, name FROM customers')
        .fetchall()
    ) == [('1', 'customer')]


def test_transaction_rollback() -> None:
    transaction_planner = Container.planners.get(TransactionCommandPlanner)
    command_planner = Container.planners.get(DataCommandPlanner)
    connection_mng = Container.managers.get(ConnectionManager)

    transaction_planner.plan_transaction(
        TransactionCommand(
            transaction_id='transaction_id',
            schema=SchemaReference(name='shippings', version=Version.LATEST),
            action=TransactionAction.BEGIN,
        )
    ).execute(transaction_id='transaction_id', lock_id=None)

    command_planner.plan_data_command(
        DataCommand(
            lock_id=None,
            transaction_id='transaction_id',
            mutations=[
                InsertData(
                    schema=SchemaReference(name='shippings', version=Version.LATEST),
                    data=[
                        Data(
                            data={'id': '111', 'customer_id': '1', 'status': 'shipped'},
                        )
                    ],
                ),
                InsertData(
                    schema=SchemaReference(name='customers', version=Version.LATEST),
                    data=[
                        Data(
                            data={'id': '1', 'name': 'customer'},
                        )
                    ],
                ),
            ],
        )
    ).execute(transaction_id='transaction_id', lock_id=None)

    transaction_planner.plan_transaction(
        TransactionCommand(
            transaction_id='transaction_id',
            schema=SchemaReference(name='shippings', version=Version.LATEST),
            action=TransactionAction.ROLLBACK,
        )
    ).execute(transaction_id='transaction_id', lock_id=None)

    assert (
        connection_mng.get_connection_pool('shippings')  # type: ignore[attr-defined]
        .get_connection()
        .execute('SELECT id, customer_id, status FROM shippings')
        .fetchall()
    ) == []
    assert (
        connection_mng.get_connection_pool('customers')  # type: ignore[attr-defined]
        .get_connection()
        .execute('SELECT id, name FROM customers')
        .fetchall()
    ) == []
