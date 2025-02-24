# mypy: disable-error-code="type-abstract"
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.interfaces.connection_manager import AsyncConnectionManager
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.services.queries import AsyncDataQueryService
from amsdal_glue_core.containers import Container

from amsdal_glue.connections.connection_pool import DefaultAsyncConnectionPool
from amsdal_glue.initialize import init_default_containers

FIXTURES_PATH = Path(__file__).parent / 'fixtures'


@pytest.fixture(autouse=True)
async def register_default_connection() -> AsyncGenerator[None, None]:
    init_default_containers()
    connection_mng = Container.managers.get(AsyncConnectionManager)

    connection_mng.register_connection_pool(
        DefaultAsyncConnectionPool(
            AsyncSqliteConnection, db_path=FIXTURES_PATH / 'customers.sqlite', check_same_thread=False
        )
    )

    connection_mng.register_connection_pool(
        DefaultAsyncConnectionPool(
            AsyncSqliteConnection, db_path=FIXTURES_PATH / 'shippings.sqlite', check_same_thread=False
        ),
        schema_name='shippings',
    )

    try:
        yield
    finally:
        await connection_mng.disconnect_all()


@pytest.mark.asyncio
async def test_data_query_service(register_default_connection: AsyncGenerator[None, None]) -> None:
    async for _ in register_default_connection:
        query = QueryStatement(
            only=[
                FieldReference(field=Field(name='id'), table_name='c'),
                FieldReference(field=Field(name='first_name'), table_name='c'),
            ],
            table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
            order_by=[
                OrderByQuery(
                    field=FieldReference(field=Field(name='id'), table_name='c'),
                    direction=OrderDirection.ASC,
                ),
            ],
        )

        service = Container.services.get(AsyncDataQueryService)
        data_result = await service.execute(
            query_op=DataQueryOperation(
                query=query,
            ),
        )
        assert data_result.success is True
        assert data_result.data
        assert [item.data if item else None for item in data_result.data] == [
            {'id': 1, 'first_name': 'John'},
            {'id': 2, 'first_name': 'Robert'},
            {'id': 3, 'first_name': 'David'},
            {'id': 4, 'first_name': 'John'},
            {'id': 5, 'first_name': 'Betty'},
        ]


@pytest.mark.asyncio
async def test_data_query_service_multiple_connections(register_default_connection: AsyncGenerator[None, None]) -> None:
    async for _ in register_default_connection:
        query = QueryStatement(
            only=[
                FieldReference(field=Field(name='id'), table_name='c'),
                FieldReference(field=Field(name='first_name'), table_name='c'),
                FieldReference(field=Field(name='status'), table_name='s'),
            ],
            table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
            joins=[
                JoinQuery(
                    table=SchemaReference(name='shippings', alias='s', version=Version.LATEST),
                    on=Conditions(
                        Condition(
                            left=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='customer_id'), table_name='s')
                            ),
                            lookup=FieldLookup.EQ,
                            right=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='id'), table_name='c')
                            ),
                        ),
                    ),
                    join_type=JoinType.INNER,
                ),
            ],
            order_by=[
                OrderByQuery(
                    field=FieldReference(field=Field(name='id'), table_name='c'),
                    direction=OrderDirection.ASC,
                ),
                OrderByQuery(
                    field=FieldReference(field=Field(name='id'), table_name='s'),
                    direction=OrderDirection.ASC,
                ),
            ],
        )

        service = Container.services.get(AsyncDataQueryService)
        data_result = await service.execute(
            query_op=DataQueryOperation(
                query=query,
            ),
        )
        assert data_result.success is True
        assert data_result.data
        assert [item.data if item else None for item in data_result.data] == [
            {'id': 1, 'first_name': 'John', 'status': 'Delivered'},
            {'id': 2, 'first_name': 'Robert', 'status': 'Pending'},
            {'id': 3, 'first_name': 'David', 'status': 'Delivered'},
            {'id': 4, 'first_name': 'John', 'status': 'Pending'},
            {'id': 5, 'first_name': 'Betty', 'status': 'Pending'},
        ]
