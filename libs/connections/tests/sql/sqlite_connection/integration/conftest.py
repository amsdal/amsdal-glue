import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection


@pytest.fixture(scope='function')
def database_connection() -> Generator[SqliteConnection, None, None]:
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / 'test.db'

        connection = SqliteConnection()
        connection.connect(db_path=db_path)

        try:
            yield connection
        finally:
            connection.disconnect()
