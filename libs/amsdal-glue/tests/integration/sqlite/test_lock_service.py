# mypy: disable-error-code="type-abstract"
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import LockAction
from amsdal_glue_core.common.enums import LockMode
from amsdal_glue_core.common.enums import LockParameter
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.common.operations.commands import LockCommand
from amsdal_glue_core.common.operations.commands import LockSchemaReference
from amsdal_glue_core.common.services.commands import LockCommandService
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
            'CREATE TABLE IF NOT EXISTS shippings (id TEXT, customer_id TEXT, status TEXT)',
        )
        connection_mng.get_connection_pool('customers').get_connection().execute(  # type: ignore[attr-defined]
            'CREATE TABLE IF NOT EXISTS customers (id TEXT, name TEXT)',
        )

        try:
            yield
        finally:
            connection_mng.disconnect_all()


def test_lock_service() -> None:
    lock_service = Container.services.get(LockCommandService)
    lock_result = lock_service.execute(
        LockCommand(
            lock_id=None,
            transaction_id=None,
            action=LockAction.ACQUIRE,
            mode=LockMode.EXCLUSIVE,
            parameter=LockParameter.SKIP_LOCKED,
            locked_objects=[LockSchemaReference(schema=SchemaReference(name='customers', version=Version.LATEST))],
        )
    )
    assert lock_result.success is True
    assert lock_result.result is True
