# mypy: disable-error-code="type-abstract"
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection
from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.annotation import ExpressionAnnotation
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.group_by import GroupByQuery
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.aggregation import Sum
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
        DefaultAsyncConnectionPool(AsyncSqliteConnection, db_path=FIXTURES_PATH / 'cities_2.sqlite'),
        schema_name='cities',
    )

    connection_mng.register_connection_pool(
        DefaultAsyncConnectionPool(AsyncSqliteConnection, db_path=FIXTURES_PATH / 'countries_2.sqlite'),
        schema_name='countries',
    )

    try:
        yield
    finally:
        await connection_mng.disconnect_all()


sum_city_population_query = QueryStatement(
    only=[
        FieldReference(field=Field(name='country_code'), table_name='c'),
        FieldReference(field=Field(name='country_population'), table_name='c'),
    ],
    aggregations=[
        AggregationQuery(
            expression=Sum(field=FieldReference(field=Field(name='Population'), table_name='ci')),
            alias='city_population',
        ),
    ],
    table=SchemaReference(name='countries', alias='c', version=Version.LATEST),
    joins=[
        JoinQuery(
            table=SchemaReference(name='cities', alias='ci', version=Version.LATEST),
            join_type=JoinType.LEFT,
            on=Conditions(
                Condition(
                    left=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='country_code'), table_name='c')
                    ),
                    lookup=FieldLookup.EQ,
                    right=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='Country'), table_name='ci')
                    ),
                ),
            ),
        ),
    ],
    group_by=[
        GroupByQuery(
            field=FieldReference(field=Field(name='country_code'), table_name='c'),
        ),
        GroupByQuery(
            field=FieldReference(field=Field(name='country_population'), table_name='c'),
        ),
    ],
)

# Define the query to calculate non city population
final_query = QueryStatement(
    only=[
        FieldReference(field=Field(name='country_code'), table_name='c'),
        FieldReference(field=Field(name='city_population'), table_name='c'),
    ],
    annotations=[
        AnnotationQuery(
            value=ExpressionAnnotation(
                expression=FieldReference(field=Field(name='country_population'), table_name='c')
                - FieldReference(field=Field(name='city_population'), table_name='c'),
                alias='non_city_population',
            ),
        ),
    ],
    table=SubQueryStatement(
        query=sum_city_population_query,
        alias='c',
    ),
    order_by=[
        OrderByQuery(
            field=FieldReference(field=Field(name='country_code'), table_name='c'),
        ),
    ],
)


@pytest.mark.asyncio
async def test_final_query(register_default_connection: AsyncGenerator[None, None]) -> None:
    async for _ in register_default_connection:
        service = Container.services.get(AsyncDataQueryService)
        data_result = await service.execute(DataQueryOperation(query=final_query))

        if not data_result.success:
            msg = 'Failed to execute query'
            raise Exception(msg) from data_result.exception  # noqa: TRY002

        assert data_result.data
        assert len(data_result.data) == 92
        assert [item.data if item else None for item in data_result.data[:5]] == [
            {'city_population': 6721891, 'country_code': 'AF', 'non_city_population': 30450495},
            {'city_population': 4740284, 'country_code': 'AO', 'non_city_population': 26069478},
            {'city_population': 34064619, 'country_code': 'AR', 'non_city_population': 10429883},
            {'city_population': 20617835, 'country_code': 'AU', 'non_city_population': 4364853},
            {'city_population': 4360723, 'country_code': 'AZ', 'non_city_population': 5579077},
        ]
