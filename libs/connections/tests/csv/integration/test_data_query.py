import pytest
from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased
from amsdal_glue_core.common.data_models.group_by import GroupByQuery
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.aggregation import Avg
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.csv_connection import CsvConnection
from tests.csv.testcases.data_query import query_big_orders
from tests.csv.testcases.data_query import query_customers
from tests.csv.testcases.data_query import query_customers_age
from tests.csv.testcases.data_query import query_customers_expenses
from tests.csv.testcases.data_query import query_expenses_by_customer
from tests.csv.testcases.data_query import query_expenses_by_customer_with_name
from tests.csv.testcases.data_query import query_orders_for_customer
from tests.csv.testcases.data_query import query_orders_with_customers


@pytest.fixture(scope='function')
def fixture_connection(database_connection: CsvConnection) -> CsvConnection:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema=Schema(
                        name='customers',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(name='id', type=int, required=True),
                            PropertySchema(name='name', type=str, required=True),
                            PropertySchema(name='age', type=int, required=True),
                        ],
                    )
                )
            ]
        )
    )
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema=Schema(
                        name='orders',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(name='id', type=int, required=True),
                            PropertySchema(name='customer_id', type=int, required=True),
                            PropertySchema(name='amount', type=int, required=True),
                        ],
                    )
                )
            ]
        )
    )
    database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name='customers', version=Version.LATEST),
            data=[Data(data={'id': 1, 'name': 'Alice', 'age': 25})],
        ),
        InsertData(
            schema=SchemaReference(name='customers', version=Version.LATEST),
            data=[Data(data={'id': 2, 'name': 'Bob', 'age': 25})],
        ),
        InsertData(
            schema=SchemaReference(name='customers', version=Version.LATEST),
            data=[Data(data={'id': 3, 'name': 'Charlie', 'age': 35})],
        ),
        InsertData(
            schema=SchemaReference(name='orders', version=Version.LATEST),
            data=[Data(data={'id': 1, 'customer_id': 1, 'amount': 100})],
        ),
        InsertData(
            schema=SchemaReference(name='orders', version=Version.LATEST),
            data=[Data(data={'id': 2, 'customer_id': 1, 'amount': 200})],
        ),
        InsertData(
            schema=SchemaReference(name='orders', version=Version.LATEST),
            data=[Data(data={'id': 3, 'customer_id': 2, 'amount': 400})],
        ),
    ])
    return database_connection


def test_simple_query(fixture_connection: CsvConnection) -> None:
    result_data = query_customers(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'name': 'Alice', 'age': 25},
        {'id': 2, 'name': 'Bob', 'age': 25},
        {'id': 3, 'name': 'Charlie', 'age': 35},
    ]


def test_join_query(fixture_connection: CsvConnection) -> None:
    result_data = query_orders_with_customers(fixture_connection, join_type=JoinType.INNER)

    assert [d.data for d in result_data] == [
        {'id': 1, 'amount': 100, 'customer_id': 1, 'name': 'Alice', 'age': 25},
        {'id': 2, 'amount': 200, 'customer_id': 1, 'name': 'Alice', 'age': 25},
        {'id': 3, 'amount': 400, 'customer_id': 2, 'name': 'Bob', 'age': 25},
    ]

    result_data = query_orders_with_customers(fixture_connection, join_type=JoinType.LEFT)

    assert [d.data for d in result_data] == [
        {'id': 1, 'amount': 100, 'customer_id': 1, 'name': 'Alice', 'age': 25},
        {'id': 2, 'amount': 200, 'customer_id': 1, 'name': 'Alice', 'age': 25},
        {'id': 3, 'amount': 400, 'customer_id': 2, 'name': 'Bob', 'age': 25},
    ]

    result_data = query_orders_with_customers(fixture_connection, join_type=JoinType.RIGHT)

    assert [d.data for d in result_data] == [
        {'id': 1.0, 'amount': 100.0, 'customer_id': 1.0, 'name': 'Alice', 'age': 25},
        {'id': 2.0, 'amount': 200.0, 'customer_id': 1.0, 'name': 'Alice', 'age': 25},
        {'id': 3.0, 'amount': 400.0, 'customer_id': 2.0, 'name': 'Bob', 'age': 25},
        {'id': None, 'amount': None, 'customer_id': None, 'name': 'Charlie', 'age': 35},
    ]

    result_data = query_orders_with_customers(fixture_connection, join_type=JoinType.FULL)

    assert [d.data for d in result_data] == [
        {'id': 1.0, 'amount': 100.0, 'customer_id': 1.0, 'name': 'Alice', 'age': 25},
        {'id': 2.0, 'amount': 200.0, 'customer_id': 1.0, 'name': 'Alice', 'age': 25},
        {'id': 3.0, 'amount': 400.0, 'customer_id': 2.0, 'name': 'Bob', 'age': 25},
        {'id': None, 'amount': None, 'customer_id': None, 'name': 'Charlie', 'age': 35},
    ]


def test_query_distinct(fixture_connection: CsvConnection) -> None:
    result_data = query_customers_age(fixture_connection)

    assert [d.data for d in result_data] == [
        {'age': 25},
        {'age': 25},
        {'age': 35},
    ]

    result_data = query_customers_age(fixture_connection, distinct=True)

    assert [d.data for d in result_data] == [
        {'age': 25},
        {'age': 35},
    ]


def test_filter_conditions(fixture_connection: CsvConnection) -> None:
    result_data = query_big_orders(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 2, 'amount': 200, 'customer_id': 1},
        {'id': 3, 'amount': 400, 'customer_id': 2},
    ]


def test_filter_conditions_join(fixture_connection: CsvConnection) -> None:
    result_data = query_orders_for_customer(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'amount': 100, 'customer_id': 1, 'age': 25},
        {'id': 2, 'amount': 200, 'customer_id': 1, 'age': 25},
    ]


def test_annotation(fixture_connection: CsvConnection) -> None:
    result_data = query_customers_expenses(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'total_amount': 300},
        {'id': 2, 'total_amount': 400},
        {'id': 3, 'total_amount': 0},
    ]


def test_aggregation(fixture_connection: CsvConnection) -> None:
    result_data = query_expenses_by_customer(fixture_connection)

    assert [d.data for d in result_data] == [
        {'customer_id': 1, 'total_amount': 300},
        {'customer_id': 2, 'total_amount': 400},
    ]


def test_aggregation_join(fixture_connection: CsvConnection) -> None:
    result_data = query_expenses_by_customer_with_name(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'name': 'Alice', 'sum_amount': 300},
        {'id': 2, 'name': 'Bob', 'sum_amount': 400},
    ]


def test_aggregation_join_existing(existing_database_connection: CsvConnection) -> None:
    result_data = existing_database_connection.query(
        query=QueryStatement(
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
        ),
    )

    assert [d.data for d in result_data] == [
        {'device_id': 1, 'name': 'device1', 'average_temp': 17.5},
        {'device_id': 2, 'name': 'device2', 'average_temp': 24.0},
        {'device_id': 3, 'name': 'device3', 'average_temp': 20.0},
        {'device_id': 5, 'name': 'device5', 'average_temp': 11.0},
    ]


def test_multiple_joins(existing_database_connection: CsvConnection) -> None:
    query = QueryStatement(
        table=SchemaReference(name='devices', version=Version.LATEST),
        only=[
            FieldReference(field=Field(name='name'), table_name='devices'),
            FieldReference(field=Field(name='name'), table_name='locations'),
            FieldReference(field=Field(name='name'), table_name='models'),
        ],
        order_by=[
            OrderByQuery(
                field=FieldReference(field=Field(name='device_id'), table_name='devices'),
                direction=OrderDirection.ASC,
            ),
        ],
        joins=[
            JoinQuery(
                table=SchemaReference(name='locations', version=Version.LATEST),
                on=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='location_id'), table_name='devices')
                        ),
                        lookup=FieldLookup.EQ,
                        right=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='location_id'), table_name='locations')
                        ),
                    ),
                ),
                join_type=JoinType.INNER,
            ),
            JoinQuery(
                table=SchemaReference(name='models', version=Version.LATEST),
                on=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='model_id'), table_name='devices')
                        ),
                        lookup=FieldLookup.EQ,
                        right=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='model_id'), table_name='models')
                        ),
                    ),
                ),
                join_type=JoinType.INNER,
            ),
        ],
    )
    result_data = existing_database_connection.query(query=query)

    assert [d.data for d in result_data] == [
        {'name': 'model1'},
        {'name': 'model2'},
        {'name': 'model3'},
        {'name': 'model1'},
        {'name': 'model2'},
        {'name': 'model3'},
    ]

    query.only = [
        FieldReference(field=Field(name='name'), table_name='devices'),
        FieldReferenceAliased(field=Field(name='name'), table_name='locations', alias='location_name'),
        FieldReferenceAliased(field=Field(name='name'), table_name='models', alias='model_name'),
    ]
    result_data = existing_database_connection.query(query=query)

    assert [d.data for d in result_data] == [
        {'name': 'device1', 'location_name': 'location1', 'model_name': 'model1'},
        {'name': 'device2', 'location_name': 'location2', 'model_name': 'model2'},
        {'name': 'device3', 'location_name': 'location1', 'model_name': 'model3'},
        {'name': 'device4', 'location_name': 'location2', 'model_name': 'model1'},
        {'name': 'device5', 'location_name': 'location1', 'model_name': 'model2'},
        {'name': 'device6', 'location_name': 'location3', 'model_name': 'model3'},
    ]
