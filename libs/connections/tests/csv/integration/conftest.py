import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

from amsdal_glue_connections.sql.connections.csv_connection import CsvConnection


@pytest.fixture(scope='function')
def database_connection() -> Generator[CsvConnection, None, None]:
    Path('.tmp').mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory(dir='.tmp') as temp_dir:
        db_path = Path(temp_dir)

        connection = CsvConnection()
        connection.connect(db_path=db_path)

        try:
            yield connection
        finally:
            connection.disconnect()
