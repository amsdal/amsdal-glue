import tempfile
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest

from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection


@pytest.fixture(scope='function')
async def database_connection() -> AsyncGenerator[AsyncSqliteConnection, None]:
    with tempfile.TemporaryDirectory(dir='.') as temp_dir:
        db_path = Path(temp_dir) / 'test.db'

        connection = AsyncSqliteConnection()
        await connection.connect(db_path=db_path)

        try:
            yield connection
        finally:
            await connection.disconnect()
