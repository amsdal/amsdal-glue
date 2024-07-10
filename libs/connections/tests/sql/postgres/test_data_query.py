from collections.abc import Generator

import pytest
from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
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
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.aggregation import Sum
from amsdal_glue_core.common.expressions.value import Value


@pytest.fixture(scope='function')
def fixture_connection(database_connection: PostgresConnection) -> Generator[PostgresConnection, None, None]:
    database_connection.execute('CREATE TABLE customers (id SERIAL PRIMARY KEY, name VARCHAR(255), age INT)')
    database_connection.execute('CREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INT, amount INT, date DATE)')
    database_connection.execute('INSERT INTO customers (id, name, age) VALUES (%s, %s, %s)', 1, 'Alice', 25)
    database_connection.execute('INSERT INTO customers (id, name, age) VALUES (%s, %s, %s)', 2, 'Bob', 25)
    database_connection.execute('INSERT INTO customers (id, name, age) VALUES (%s, %s, %s)', 3, 'Charlie', 35)
    database_connection.execute('INSERT INTO orders (id, customer_id, amount) VALUES (%s, %s, %s)', 1, 1, 100)
    database_connection.execute('INSERT INTO orders (id, customer_id, amount) VALUES (%s, %s, %s)', 2, 1, 200)
    database_connection.execute('INSERT INTO orders (id, customer_id, amount) VALUES (%s, %s, %s)', 3, 2, 400)

    yield database_connection


def test_simple_query_data(fixture_connection: PostgresConnection) -> None:
    result_data = fixture_connection.query(
        QueryStatement(
            table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
            order_by=[
                OrderByQuery(
                    field=FieldReference(field=Field(name='id'), table_name='c'),
                    direction=OrderDirection.ASC,
                ),
            ],
        )
    )

    assert [d.data for d in result_data] == [
        {'id': 1, 'name': 'Alice', 'age': 25},
        {'id': 2, 'name': 'Bob', 'age': 25},
        {'id': 3, 'name': 'Charlie', 'age': 35},
    ]


def test_join_query_data(fixture_connection: PostgresConnection) -> None:
    result_data = fixture_connection.query(
        QueryStatement(
            table=SchemaReference(name='orders', alias='o', version=Version.LATEST),
            order_by=[
                OrderByQuery(
                    field=FieldReference(field=Field(name='id'), table_name='o'),
                    direction=OrderDirection.ASC,
                ),
            ],
            only=[
                FieldReference(field=Field(name='id'), table_name='o'),
                FieldReference(field=Field(name='amount'), table_name='o'),
                FieldReference(field=Field(name='customer_id'), table_name='o'),
                FieldReference(field=Field(name='name'), table_name='c'),
                FieldReference(field=Field(name='age'), table_name='c'),
            ],
            joins=[
                JoinQuery(
                    table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
                    on=Conditions(
                        Condition(
                            field=FieldReference(field=Field(name='customer_id'), table_name='o'),
                            lookup=FieldLookup.EQ,
                            value=FieldReference(field=Field(name='id'), table_name='c'),
                        ),
                    ),
                    join_type=JoinType.INNER,
                ),
            ],
        )
    )
    assert [d.data for d in result_data] == [
        {'id': 1, 'amount': 100, 'customer_id': 1, 'name': 'Alice', 'age': 25},
        {'id': 2, 'amount': 200, 'customer_id': 1, 'name': 'Alice', 'age': 25},
        {'id': 3, 'amount': 400, 'customer_id': 2, 'name': 'Bob', 'age': 25},
    ]


def test_select_distinct(fixture_connection: PostgresConnection) -> None:
    query = QueryStatement(
        table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
        only=[
            FieldReference(field=Field(name='age'), table_name='c'),
        ],
        order_by=[
            OrderByQuery(
                field=FieldReference(field=Field(name='age'), table_name='c'),
                direction=OrderDirection.ASC,
            ),
        ],
    )
    result_data = fixture_connection.query(query)

    assert [d.data for d in result_data] == [
        {'age': 25},
        {'age': 25},
        {'age': 35},
    ]

    query.distinct = True
    result_data = fixture_connection.query(query)

    assert [d.data for d in result_data] == [
        {'age': 25},
        {'age': 35},
    ]


def test_filter_query_data(fixture_connection: PostgresConnection) -> None:
    result_data = fixture_connection.query(
        QueryStatement(
            table=SchemaReference(name='orders', alias='o', version=Version.LATEST),
            order_by=[
                OrderByQuery(
                    field=FieldReference(field=Field(name='id'), table_name='o'),
                    direction=OrderDirection.ASC,
                ),
            ],
            only=[
                FieldReference(field=Field(name='id'), table_name='o'),
                FieldReference(field=Field(name='amount'), table_name='o'),
                FieldReference(field=Field(name='customer_id'), table_name='o'),
            ],
            where=Conditions(
                Condition(
                    field=FieldReference(field=Field(name='amount'), table_name='o'),
                    lookup=FieldLookup.GT,
                    value=Value(100),
                ),
            ),
        )
    )
    assert [d.data for d in result_data] == [
        {'id': 2, 'amount': 200, 'customer_id': 1},
        {'id': 3, 'amount': 400, 'customer_id': 2},
    ]


def test_filter_nested_query_data(fixture_connection: PostgresConnection) -> None:
    result_data = fixture_connection.query(
        QueryStatement(
            table=SchemaReference(name='orders', alias='o', version=Version.LATEST),
            order_by=[
                OrderByQuery(
                    field=FieldReference(field=Field(name='id'), table_name='o'),
                    direction=OrderDirection.ASC,
                ),
            ],
            only=[
                FieldReference(field=Field(name='id'), table_name='o'),
                FieldReference(field=Field(name='amount'), table_name='o'),
                FieldReference(field=Field(name='customer_id'), table_name='o'),
                FieldReference(field=Field(name='age'), table_name='c'),
            ],
            joins=[
                JoinQuery(
                    table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
                    on=Conditions(
                        Condition(
                            field=FieldReference(field=Field(name='customer_id'), table_name='o'),
                            lookup=FieldLookup.EQ,
                            value=FieldReference(field=Field(name='id'), table_name='c'),
                        ),
                    ),
                    join_type=JoinType.INNER,
                ),
            ],
            where=Conditions(
                Condition(
                    field=FieldReference(field=Field(name='name'), table_name='c'),
                    lookup=FieldLookup.EQ,
                    value=Value('Alice'),
                ),
            ),
        )
    )
    assert [d.data for d in result_data] == [
        {'id': 1, 'amount': 100, 'customer_id': 1, 'age': 25},
        {'id': 2, 'amount': 200, 'customer_id': 1, 'age': 25},
    ]


def test_annotation_query(fixture_connection: PostgresConnection) -> None:
    result_data = fixture_connection.query(
        QueryStatement(
            only=[
                FieldReference(field=Field(name='id'), table_name='c'),
            ],
            annotations=[
                AnnotationQuery(
                    value=SubQueryStatement(
                        alias='total_amount',
                        query=QueryStatement(
                            aggregations=[
                                AggregationQuery(
                                    expression=Sum(
                                        field=FieldReference(field=Field(name='amount'), table_name='o'),
                                    ),
                                    alias='total_amount',
                                ),
                            ],
                            table=SchemaReference(name='orders', alias='o', version=Version.LATEST),
                            where=Conditions(
                                Condition(
                                    field=FieldReference(field=Field(name='customer_id'), table_name='o'),
                                    lookup=FieldLookup.EQ,
                                    value=FieldReference(field=Field(name='id'), table_name='c'),
                                ),
                            ),
                        ),
                    ),
                ),
            ],
            table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
            order_by=[
                OrderByQuery(
                    field=FieldReference(field=Field(name='id'), table_name='c'),
                    direction=OrderDirection.ASC,
                ),
            ],
        )
    )

    assert [d.data for d in result_data] == [
        {'id': 1, 'total_amount': 300},
        {'id': 2, 'total_amount': 400},
        {'id': 3, 'total_amount': None},
    ]


def test_aggregation_query(fixture_connection: PostgresConnection) -> None:
    result_data = fixture_connection.query(
        query=QueryStatement(
            only=[
                FieldReference(field=Field(name='customer_id'), table_name='o'),
            ],
            aggregations=[
                AggregationQuery(
                    expression=Sum(
                        field=FieldReference(field=Field(name='amount'), table_name='o'),
                    ),
                    alias='total_amount',
                ),
            ],
            table=SchemaReference(name='orders', alias='o', version=Version.LATEST),
            group_by=[
                GroupByQuery(field=FieldReference(field=Field(name='customer_id'), table_name='o')),
            ],
            order_by=[
                OrderByQuery(
                    field=FieldReference(field=Field(name='customer_id'), table_name='o'),
                    direction=OrderDirection.ASC,
                ),
            ],
        ),
    )
    assert [d.data for d in result_data] == [
        {'customer_id': 1, 'total_amount': 300},
        {'customer_id': 2, 'total_amount': 400},
    ]


def test_aggregation_query_joins(fixture_connection: PostgresConnection) -> None:
    result_data = fixture_connection.query(
        query=QueryStatement(
            table=SchemaReference(name='orders', version=Version.LATEST),
            only=[
                FieldReference(field=Field(name='id'), table_name='customers'),
                FieldReference(field=Field(name='name'), table_name='customers'),
            ],
            joins=[
                JoinQuery(
                    table=SchemaReference(name='customers', version=Version.LATEST),
                    on=Conditions(
                        Condition(
                            field=FieldReference(field=Field(name='id'), table_name='customers'),
                            lookup=FieldLookup.EQ,
                            value=FieldReference(field=Field(name='customer_id'), table_name='orders'),
                        ),
                    ),
                    join_type=JoinType.INNER,
                ),
            ],
            aggregations=[
                AggregationQuery(
                    expression=Sum(field=FieldReference(field=Field(name='amount'), table_name='orders')),
                    alias='sum_amount',
                ),
            ],
            group_by=[
                GroupByQuery(field=FieldReference(field=Field(name='id'), table_name='customers')),
                GroupByQuery(field=FieldReference(field=Field(name='name'), table_name='customers')),
            ],
            order_by=[
                OrderByQuery(
                    field=FieldReference(field=Field(name='id'), table_name='customers'),
                    direction=OrderDirection.ASC,
                ),
            ],
        ),
    )
    assert [d.data for d in result_data] == [
        {'id': 1, 'name': 'Alice', 'sum_amount': 300},
        {'id': 2, 'name': 'Bob', 'sum_amount': 400},
    ]
