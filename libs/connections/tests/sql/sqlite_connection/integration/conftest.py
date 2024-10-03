import tempfile
from pathlib import Path
from typing import Generator

import pytest

import amsdal_glue as glue


@pytest.fixture(scope='function')
def database_connection() -> Generator[glue.SqliteConnection, None, None]:
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / 'test.db'

        connection = glue.SqliteConnection()
        connection.connect(db_path=db_path)

        try:
            yield connection
        finally:
            connection.disconnect()
