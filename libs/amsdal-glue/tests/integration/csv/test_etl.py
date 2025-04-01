# mypy: disable-error-code="type-abstract"
from collections.abc import Generator
from pathlib import Path

import pytest
from amsdal_glue_connections.sql.connections.csv_connection import CsvConnection
from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.group_by import GroupByQuery
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.aggregation import Avg
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.services.queries import DataQueryService
from amsdal_glue_core.containers import Container

from amsdal_glue.connections.connection_pool import DefaultConnectionPool
from amsdal_glue.initialize import init_default_containers

FIXTURES_PATH = Path(__file__).parent / 'fixtures'


@pytest.fixture(autouse=True)
def _register_default_connection() -> Generator[None, None, None]:
    init_default_containers()
    connection_mng = Container.managers.get(ConnectionManager)

    connection_mng.register_connection_pool(
        DefaultConnectionPool(CsvConnection, db_path=FIXTURES_PATH / 'data1'),
        schema_name='logs',
    )
    connection_mng.register_connection_pool(
        DefaultConnectionPool(CsvConnection, db_path=FIXTURES_PATH / 'data2'),
    )

    try:
        yield
    finally:
        connection_mng.disconnect_all()


@pytest.mark.skip
def test_aggregation() -> None:
    expressions_query = QueryStatement(
        table=SchemaReference(name='logs', version=Version.LATEST),
        only=[
            FieldReference(field=Field(name='device_id'), table_name='logs'),
            FieldReference(field=Field(name='temp_log'), table_name='logs'),
            FieldReference(field=Field(name='name'), table_name='devices'),
        ],
        aggregations=[
            AggregationQuery(
                expression=Avg(
                    field=FieldReference(field=Field(name='temp_log'), table_name='logs'),
                ),
                alias='average_temp',
            ),
        ],
        group_by=[
            GroupByQuery(field=FieldReference(field=Field(name='device_id'), table_name='logs')),
            GroupByQuery(field=FieldReference(field=Field(name='name'), table_name='devices')),
        ],
        order_by=[
            OrderByQuery(
                field=FieldReference(field=Field(name='device_id'), table_name='devices'),
                direction=OrderDirection.ASC,
            ),
        ],
        joins=[
            JoinQuery(
                table=SchemaReference(name='devices', version=Version.LATEST),
                on=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='device_id'), table_name='logs')
                        ),
                        lookup=FieldLookup.EQ,
                        right=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='device_id'), table_name='devices')
                        ),
                    ),
                ),
                join_type=JoinType.INNER,
            )
        ],
    )
    service = Container.services.get(DataQueryService)
    data_result = service.execute(DataQueryOperation(query=expressions_query))

    if not data_result.success:
        msg = 'Failed to execute query'
        raise Exception(msg) from data_result.exception  # noqa: TRY002

    assert [d.data for d in (data_result.data or [])] == [
        {'device_id': 1, 'name': 'device1', 'average_temp': 17.5},
        {'device_id': 2, 'name': 'device2', 'average_temp': 24.0},
        {'device_id': 3, 'name': 'device3', 'average_temp': 20.0},
        {'device_id': 5, 'name': 'device5', 'average_temp': 11.0},
    ]
