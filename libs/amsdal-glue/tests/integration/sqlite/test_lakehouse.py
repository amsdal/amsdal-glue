# mypy: disable-error-code="type-abstract"
import tempfile
from collections.abc import Generator

import pytest
from pytest_mock import MockerFixture

from amsdal_glue import Container
from amsdal_glue import Data
from amsdal_glue import DataCommand
from amsdal_glue import DataQueryOperation
from amsdal_glue import DefaultConnectionPool
from amsdal_glue import Field
from amsdal_glue import FieldReference
from amsdal_glue import InsertData
from amsdal_glue import OrderByQuery
from amsdal_glue import OrderDirection
from amsdal_glue import QueryStatement
from amsdal_glue import RegisterSchema
from amsdal_glue import SchemaCommand
from amsdal_glue import SchemaReference
from amsdal_glue import SqliteConnection
from amsdal_glue import Version
from amsdal_glue.applications.lakehouse import LakehouseApplication
from amsdal_glue.interfaces import DataCommandService
from amsdal_glue.interfaces import DataQueryService
from amsdal_glue.interfaces import RuntimeManager
from amsdal_glue.interfaces import SchemaCommandService


@pytest.fixture()
def lakehouse_app() -> Generator[LakehouseApplication, None, None]:
    app = LakehouseApplication()

    with tempfile.TemporaryDirectory() as temp_dir:
        query_db_path = f'{temp_dir}/query_data.sqlite'
        command_db_path = f'{temp_dir}/command_data.sqlite'

        app.default_connection_manager.register_connection_pool(
            DefaultConnectionPool(
                SqliteConnection,
                db_path=query_db_path,
            ),
        )
        app.lakehouse_connection_manager.register_connection_pool(
            DefaultConnectionPool(
                SqliteConnection,
                db_path=command_db_path,
            ),
        )

        for connection_manager in [app.default_connection_manager, app.lakehouse_connection_manager]:
            connection_manager.get_connection_pool('customers').get_connection().execute(  # type: ignore[attr-defined]
                'CREATE TABLE IF NOT EXISTS customers (id TEXT, name TEXT)',
            )

        try:
            yield app
        finally:
            app.shutdown()


def test_schema_command(lakehouse_app: LakehouseApplication) -> None:
    from .fixtures.user_schema import user_schema

    service = Container.services.get(SchemaCommandService)
    result = service.execute(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=user_schema),
            ],
        ),
    )

    # wait for the runtime to finish
    runtime = Container.managers.get(RuntimeManager)
    runtime.shutdown()

    assert result.success is True
    assert result.schemas == [None]

    connections = [
        lakehouse_app.default_connection_manager.get_connection_pool(user_schema.name).get_connection(),
        lakehouse_app.lakehouse_connection_manager.get_connection_pool(user_schema.name).get_connection(),
    ]

    # check table was created in both connections
    for connection in connections:
        cursor = connection.execute(f'PRAGMA table_info({user_schema.name})')  # type: ignore[attr-defined]
        columns = cursor.fetchall()
        cursor.close()

        assert len(columns) == 5


def test_data_command(lakehouse_app: LakehouseApplication):
    service = Container.services.get(DataCommandService)
    result = service.execute(
        DataCommand(
            mutations=[
                InsertData(
                    schema=SchemaReference(name='customers', version=Version.LATEST),
                    data=[
                        Data(data={'id': '1', 'name': 'Alice'}),
                        Data(data={'id': '2', 'name': 'Bob'}),
                    ],
                ),
            ],
        ),
    )

    assert result.success is True

    connections = [
        lakehouse_app.default_connection_manager.get_connection_pool('customers').get_connection(),
        lakehouse_app.lakehouse_connection_manager.get_connection_pool('customers').get_connection(),
    ]

    # check records were created in both connections
    for connection in connections:
        cursor = connection.execute('SELECT * FROM customers ORDER BY id')  # type: ignore[attr-defined]
        records = cursor.fetchall()
        cursor.close()

        assert records == [('1', 'Alice'), ('2', 'Bob')]


def test_data_query(lakehouse_app: LakehouseApplication, mocker: MockerFixture):
    service = Container.services.get(DataCommandService)

    result = service.execute(
        DataCommand(
            mutations=[
                InsertData(
                    schema=SchemaReference(name='customers', version=Version.LATEST),
                    data=[
                        Data(data={'id': '1', 'name': 'Alice'}),
                        Data(data={'id': '2', 'name': 'Bob'}),
                    ],
                ),
            ],
        ),
    )

    assert result.success is True

    # wait for the runtime to finish
    runtime = Container.managers.get(RuntimeManager)
    runtime.shutdown()

    mocked_command_connection_pool = mocker.Mock(spec=DefaultConnectionPool)
    lakehouse_app.lakehouse_connection_manager.register_connection_pool(mocked_command_connection_pool)

    query_service = Container.services.get(DataQueryService)
    query = QueryStatement(
        table=SchemaReference(name='customers', version=Version.LATEST),
        order_by=[
            OrderByQuery(
                field=FieldReference(field=Field(name='id'), table_name='customers'),
                direction=OrderDirection.ASC,
            ),
        ],
    )
    data_result = query_service.execute(
        query_op=DataQueryOperation(
            query=query,
        ),
    )
    assert data_result.success is True
    assert data_result.data
    assert [item.data if item else None for item in data_result.data] == [
        {'id': '1', 'name': 'Alice'},
        {'id': '2', 'name': 'Bob'},
    ]
    assert mocked_command_connection_pool.get_connection.called is False
