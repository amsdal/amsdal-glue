# mypy: disable-error-code="type-abstract"
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from amsdal_glue.initialize import init_default_containers
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_core.commands.planner.data_command_planner import DataCommandPlanner
from amsdal_glue_core.commands.planner.transaction_command_planner import TransactionCommandPlanner
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.metadata import Metadata
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import TransactionAction
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.helpers.singleton import Singleton
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.services.managers.connection import ConnectionManager
from amsdal_glue_core.containers import Container


@pytest.fixture(autouse=True)
def _register_default_connection() -> Generator[None, None, None]:
    init_default_containers()
    shipping_connection = SqliteConnection()
    connection_mng = Container.managers.get(ConnectionManager)
    connection_mng.register_connection(shipping_connection, schema_name='shippings')
    connection_mng.register_connection(shipping_connection, schema_name='customers')

    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = f'{temp_dir}/data.sqlite'
        shipping_connection.connect(db_path=Path(db_path), check_same_thread=False)

        shipping_connection.execute('CREATE TABLE IF NOT EXISTS shippings (id TEXT, customer_id TEXT, status TEXT)')
        shipping_connection.execute('CREATE TABLE IF NOT EXISTS customers (id TEXT, name TEXT)')

        yield

        shipping_connection.disconnect()

    Singleton.invalidate_all_instances()


def test_transaction() -> None:
    transaction_planner = Container.planners.get(TransactionCommandPlanner)
    command_planner = Container.planners.get(DataCommandPlanner)

    transaction_planner.plan_transaction(
        TransactionCommand(
            transaction_id='transaction_id',
            schema=SchemaReference(name='shippings', version=Version.LATEST),
            action=TransactionAction.BEGIN,
        )
    ).execute()

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
                            metadata=Metadata(
                                object_id='1',
                                object_version='1',
                                created_at='2021-01-01T00:00:00Z',
                                updated_at='2021-01-01T00:00:00Z',
                            ),
                        )
                    ],
                ),
                InsertData(
                    schema=SchemaReference(name='customers', version=Version.LATEST),
                    data=[
                        Data(
                            data={'id': '1', 'name': 'customer'},
                            metadata=Metadata(
                                object_id='1',
                                object_version='1',
                                created_at='2021-01-01T00:00:00Z',
                                updated_at='2021-01-01T00:00:00Z',
                            ),
                        )
                    ],
                ),
            ],
        )
    ).execute()

    transaction_planner.plan_transaction(
        TransactionCommand(
            transaction_id='transaction_id',
            schema=SchemaReference(name='shippings', version=Version.LATEST),
            action=TransactionAction.COMMIT,
        )
    ).execute()

    assert (
        [('111', '1', 'shipped')]
        == ConnectionManager()  # type: ignore[attr-defined]
        .get_connection('shippings')
        .execute('SELECT id, customer_id, status FROM shippings')
        .fetchall()
    )
    assert [('1', 'customer')] == (
        ConnectionManager()  # type: ignore[attr-defined]
        .get_connection('customers')
        .execute('SELECT id, name FROM customers')
        .fetchall()
    )


def test_transaction_rollback() -> None:
    transaction_planner = Container.planners.get(TransactionCommandPlanner)
    command_planner = Container.planners.get(DataCommandPlanner)

    transaction_planner.plan_transaction(
        TransactionCommand(
            transaction_id='transaction_id',
            schema=SchemaReference(name='shippings', version=Version.LATEST),
            action=TransactionAction.BEGIN,
        )
    ).execute()

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
                            metadata=Metadata(
                                object_id='1',
                                object_version='1',
                                created_at='2021-01-01T00:00:00Z',
                                updated_at='2021-01-01T00:00:00Z',
                            ),
                        )
                    ],
                ),
                InsertData(
                    schema=SchemaReference(name='customers', version=Version.LATEST),
                    data=[
                        Data(
                            data={'id': '1', 'name': 'customer'},
                            metadata=Metadata(
                                object_id='1',
                                object_version='1',
                                created_at='2021-01-01T00:00:00Z',
                                updated_at='2021-01-01T00:00:00Z',
                            ),
                        )
                    ],
                ),
            ],
        )
    ).execute()

    transaction_planner.plan_transaction(
        TransactionCommand(
            transaction_id='transaction_id',
            schema=SchemaReference(name='shippings', version=Version.LATEST),
            action=TransactionAction.ROLLBACK,
        )
    ).execute()

    assert [] == (
        ConnectionManager()  # type: ignore[attr-defined]
        .get_connection('shippings')
        .execute('SELECT id, customer_id, status FROM shippings')
        .fetchall()
    )
    assert [] == (
        ConnectionManager()  # type: ignore[attr-defined]
        .get_connection('customers')
        .execute('SELECT id, name FROM customers')
        .fetchall()
    )