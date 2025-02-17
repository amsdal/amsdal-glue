# mypy: disable-error-code="type-abstract"
from collections.abc import Generator
from pathlib import Path

import pytest
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
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
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.services.queries import DataQueryService
from amsdal_glue_core.containers import Container

from amsdal_glue import FieldReferenceAliased
from amsdal_glue.connections.connection_pool import DefaultConnectionPool
from amsdal_glue.initialize import init_default_containers

FIXTURES_PATH = Path(__file__).parent / 'fixtures'


@pytest.fixture(autouse=True)
def _register_default_connection() -> Generator[None, None, None]:
    init_default_containers()
    connection_mng = Container.managers.get(ConnectionManager)

    connection_mng.register_connection_pool(
        DefaultConnectionPool(SqliteConnection, db_path=FIXTURES_PATH / 'cities.sqlite'),
        schema_name='cities',
    )

    connection_mng.register_connection_pool(
        DefaultConnectionPool(SqliteConnection, db_path=FIXTURES_PATH / 'countries.sqlite'),
        schema_name='countries',
    )

    connection_mng.register_connection_pool(
        DefaultConnectionPool(SqliteConnection, db_path=FIXTURES_PATH / 'countries_map.sqlite'),
    )

    try:
        yield
    finally:
        connection_mng.disconnect_all()


cities_with_country_code_query = QueryStatement(
    only=[
        FieldReferenceAliased(field=Field(name='country_code'), table_name='cm', alias='country_code'),
        FieldReferenceAliased(field=Field(name='Country'), table_name='c', alias='country_name'),
        FieldReferenceAliased(field=Field(name='City'), table_name='c', alias='city_name'),
        FieldReferenceAliased(field=Field(name='CityPopulation'), table_name='c', alias='city_population'),
    ],
    table=SchemaReference(name='cities', alias='c', version=Version.LATEST),
    joins=[
        JoinQuery(
            table=SchemaReference(name='countries_map', alias='cm', version=Version.LATEST),
            join_type=JoinType.LEFT,
            on=Conditions(
                Condition(
                    left=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='country_name'), table_name='cm')
                    ),
                    lookup=FieldLookup.EQ,
                    right=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='Country'), table_name='c')
                    ),
                ),
            ),
        ),
    ],
)

sum_city_population_query = QueryStatement(
    only=[
        FieldReferenceAliased(field=Field(name='country_name'), table_name='cts_codes', alias='country_name'),
        FieldReferenceAliased(field=Field(name='population'), table_name='cnt', alias='country_population'),
    ],
    aggregations=[
        AggregationQuery(
            expression=Sum(field=FieldReference(field=Field(name='city_population'), table_name='cts_codes')),
            alias='city_population',
        ),
    ],
    table=SchemaReference(name='countries', alias='cnt', version=Version.LATEST),
    joins=[
        JoinQuery(
            table=SubQueryStatement(query=cities_with_country_code_query, alias='cts_codes'),
            join_type=JoinType.LEFT,
            on=Conditions(
                Condition(
                    left=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='country_code'), table_name='cts_codes')
                    ),
                    lookup=FieldLookup.EQ,
                    right=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='country_code'), table_name='cnt')
                    ),
                ),
            ),
        ),
    ],
    group_by=[
        GroupByQuery(
            field=FieldReference(field=Field(name='country_name'), table_name='cts_codes'),
        ),
        GroupByQuery(
            field=FieldReference(field=Field(name='population'), table_name='cnt'),
        ),
    ],
    order_by=[
        OrderByQuery(
            field=FieldReference(field=Field(name='country_name'), table_name='cts_codes'),
        ),
    ],
)

sum_non_city_population_query = QueryStatement(
    only=[
        FieldReferenceAliased(field=Field(name='country_name'), table_name='pop', alias='country_name'),
        FieldReferenceAliased(field=Field(name='city_population'), table_name='pop', alias='city_population'),
        FieldReferenceAliased(field=Field(name='country_population'), table_name='pop', alias='country_population'),
    ],
    annotations=[
        AnnotationQuery(
            value=ExpressionAnnotation(
                expression=FieldReference(field=Field(name='country_population'), table_name='pop')
                - FieldReference(field=Field(name='city_population'), table_name='pop'),
                alias='non_city_population',
            ),
        ),
    ],
    table=SubQueryStatement(query=sum_city_population_query, alias='pop'),
)


def test_cities_with_country_code() -> None:
    service = Container.services.get(DataQueryService)
    data_result = service.execute(DataQueryOperation(query=cities_with_country_code_query))
    assert data_result.success is True
    assert data_result.data
    assert len(data_result.data) == 123768
    assert [item.data if item else None for item in data_result.data[:5]] == [
        {'city_name': 'Acheng', 'city_population': 144665, 'country_code': 'CN', 'country_name': 'China'},
        {'city_name': 'Aksu', 'city_population': 340020, 'country_code': 'CN', 'country_name': 'China'},
        {'city_name': 'Altay', 'city_population': 139341, 'country_code': 'CN', 'country_name': 'China'},
        {'city_name': 'Anbu', 'city_population': 162964, 'country_code': 'CN', 'country_name': 'China'},
        {'city_name': 'Anda', 'city_population': 181271, 'country_code': 'CN', 'country_name': 'China'},
    ]


def test_sum_city_population() -> None:
    service = Container.services.get(DataQueryService)
    data_result = service.execute(DataQueryOperation(query=sum_city_population_query))
    assert data_result.success is True, data_result.exception
    assert data_result.data
    assert len(data_result.data) == 92
    assert [item.data if item else None for item in data_result.data[:5]] == [
        {'city_population': 6721891, 'country_name': 'Afghanistan', 'country_population': 37172386},
        {'city_population': 4740284, 'country_name': 'Angola', 'country_population': 30809762},
        {'city_population': 34064619, 'country_name': 'Argentina', 'country_population': 44494502},
        {'city_population': 20617835, 'country_name': 'Australia', 'country_population': 24982688},
        {'city_population': 4360723, 'country_name': 'Azerbaijan', 'country_population': 9939800},
    ]


def test_non_city_population() -> None:
    service = Container.services.get(DataQueryService)
    data_result = service.execute(DataQueryOperation(query=sum_non_city_population_query))

    if not data_result.success:
        msg = 'Failed to execute query'
        raise Exception(msg) from data_result.exception  # noqa: TRY002

    assert data_result.data
    assert len(data_result.data) == 92
    assert [item.data if item else None for item in data_result.data[:5]] == [
        {
            'city_population': 6721891,
            'country_name': 'Afghanistan',
            'country_population': 37172386,
            'non_city_population': 30450495,
        },
        {
            'city_population': 4740284,
            'country_name': 'Angola',
            'country_population': 30809762,
            'non_city_population': 26069478,
        },
        {
            'city_population': 34064619,
            'country_name': 'Argentina',
            'country_population': 44494502,
            'non_city_population': 10429883,
        },
        {
            'city_population': 20617835,
            'country_name': 'Australia',
            'country_population': 24982688,
            'non_city_population': 4364853,
        },
        {
            'city_population': 4360723,
            'country_name': 'Azerbaijan',
            'country_population': 9939800,
            'non_city_population': 5579077,
        },
    ]


def test_expressions() -> None:
    expressions_query = QueryStatement(
        only=[
            FieldReferenceAliased(field=Field(name='population'), table_name='cnt', alias='country_population'),
        ],
        annotations=[
            AnnotationQuery(
                value=ExpressionAnnotation(
                    expression=FieldReference(field=Field(name='population'), table_name='cnt') + 1000,
                    alias='add',
                ),
            ),
            AnnotationQuery(
                value=ExpressionAnnotation(
                    expression=FieldReference(field=Field(name='population'), table_name='cnt') - 1000,
                    alias='sub',
                ),
            ),
            AnnotationQuery(
                value=ExpressionAnnotation(
                    expression=FieldReference(field=Field(name='population'), table_name='cnt') * 1000,
                    alias='mul',
                ),
            ),
            AnnotationQuery(
                value=ExpressionAnnotation(
                    expression=FieldReference(field=Field(name='population'), table_name='cnt') / 1000,
                    alias='div',
                ),
            ),
            AnnotationQuery(
                value=ExpressionAnnotation(
                    expression=FieldReference(field=Field(name='population'), table_name='cnt') ** 2,
                    alias='pow',
                ),
            ),
            AnnotationQuery(
                value=ExpressionAnnotation(
                    expression=FieldReference(field=Field(name='population'), table_name='cnt') % 2,
                    alias='mod',
                ),
            ),
        ],
        table=SchemaReference(name='countries', alias='cnt', version=Version.LATEST),
    )

    service = Container.services.get(DataQueryService)
    data_result = service.execute(DataQueryOperation(query=expressions_query))

    if not data_result.success:
        msg = 'Failed to execute query'
        raise Exception(msg) from data_result.exception  # noqa: TRY002

    assert [item.data if item else None for item in (data_result.data or [])[:5]] == [
        {
            'add': 1392731000,
            'country_population': 1392730000,
            'div': 1392730,
            'mod': 0,
            'mul': 1392730000000,
            'pow': 1.9396968529e18,
            'sub': 1392729000,
        },
        {
            'add': 1352618328,
            'country_population': 1352617328,
            'div': 1352617,
            'mod': 0,
            'mul': 1352617328000,
            'pow': 1.8295736360058596e18,
            'sub': 1352616328,
        },
        {
            'add': 326688501,
            'country_population': 326687501,
            'div': 326687,
            'mod': 1,
            'mul': 326687501000,
            'pow': 1.0672472330962501e17,
            'sub': 326686501,
        },
        {
            'add': 267664435,
            'country_population': 267663435,
            'div': 267663,
            'mod': 1,
            'mul': 267663435000,
            'pow': 7.1643714435999224e16,
            'sub': 267662435,
        },
        {
            'add': 212216030,
            'country_population': 212215030,
            'div': 212215,
            'mod': 0,
            'mul': 212215030000,
            'pow': 4.5035218957900904e16,
            'sub': 212214030,
        },
    ]
