# mypy: disable-error-code="type-abstract"
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.services.commands import DataCommandService
from amsdal_glue_core.containers import Container

from amsdal_glue.connections.connection_pool import DefaultConnectionPool
from amsdal_glue.initialize import init_default_containers


@pytest.fixture(autouse=True)
def _register_default_connection() -> Generator[None, None, None]:
    init_default_containers()
    connection_mng = Container.managers.get(ConnectionManager)

    with tempfile.TemporaryDirectory() as temp_dir:
        connection_mng.register_connection_pool(
            DefaultConnectionPool(SqliteConnection, db_path=Path(f'{temp_dir}/data.sqlite'), check_same_thread=False),
        )
        connection_mng.register_connection_pool(
            DefaultConnectionPool(SqliteConnection, db_path=Path(f'{temp_dir}/data.sqlite'), check_same_thread=False),
            schema_name='Customer',
        )

        connection_mng.get_connection_pool('Shipping').get_connection().execute(  # type: ignore[attr-defined]
            'CREATE TABLE IF NOT EXISTS Shipping (id TEXT, customer_id TEXT, status TEXT)',
        )

        connection_mng.get_connection_pool('Customer').get_connection().execute(  # type: ignore[attr-defined]
            'CREATE TABLE IF NOT EXISTS Customer (id TEXT, name TEXT)',
        )

        try:
            yield
        finally:
            connection_mng.disconnect_all()


def test_data_command_service() -> None:
    service = Container.services.get(DataCommandService)
    service.execute(
        command=DataCommand(
            mutations=[
                InsertData(
                    schema=SchemaReference(name='Shipping', version=Version.LATEST),
                    data=[
                        Data(
                            data={'id': 'id-1', 'customer_id': 'customer-1', 'status': 'shipped'},
                        ),
                    ],
                ),
            ],
        ),
    )
    connection_mng = Container.managers.get(ConnectionManager)
    connection = connection_mng.get_connection_pool('Shipping').get_connection()
    cursor = connection.execute('SELECT * FROM Shipping')  # type: ignore[attr-defined]
    assert cursor.fetchall() == [('id-1', 'customer-1', 'shipped')]


def test_data_command_service_multiple_databases() -> None:
    service = Container.services.get(DataCommandService)
    service.execute(
        command=DataCommand(
            mutations=[
                InsertData(
                    schema=SchemaReference(name='Shipping', version=Version.LATEST),
                    data=[
                        Data(
                            data={'id': 'id-1', 'customer_id': 'customer-1', 'status': 'shipped'},
                        ),
                    ],
                ),
                InsertData(
                    schema=SchemaReference(name='Customer', version=Version.LATEST),
                    data=[
                        Data(
                            data={'id': 'customer-1', 'name': 'John Doe'},
                        ),
                    ],
                ),
            ],
        ),
    )
    connection_mng = Container.managers.get(ConnectionManager)
    connection = connection_mng.get_connection_pool('Shipping').get_connection()
    cursor = connection.execute('SELECT * FROM Shipping')  # type: ignore[attr-defined]
    assert cursor.fetchall() == [('id-1', 'customer-1', 'shipped')]

    connection = connection_mng.get_connection_pool('Customer').get_connection()
    cursor = connection.execute('SELECT * FROM Customer')  # type: ignore[attr-defined]
    assert cursor.fetchall() == [('customer-1', 'John Doe')]
