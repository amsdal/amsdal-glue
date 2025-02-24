# mypy: disable-error-code="type-abstract"
import os
from collections.abc import Generator
from contextlib import contextmanager
from contextlib import suppress
from pathlib import Path

import psycopg
import pytest
from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from amsdal_glue_core.commands.planner.data_command_planner import DataCommandPlanner
from amsdal_glue_core.commands.planner.schema_command_planner import SchemaCommandPlanner
from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.aggregation import Sum
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.containers import Container
from amsdal_glue_core.queries.planner.data_query_planner import DataQueryPlanner

from amsdal_glue.connections.connection_pool import DefaultConnectionPool
from amsdal_glue.initialize import init_default_containers

FIXTURES_PATH = Path(__file__).parent / 'fixtures'


@contextmanager
def create_database(dsn: str, database: str) -> Generator[None, None, None]:
    conn = psycopg.connect(dsn, autocommit=True)

    with suppress(psycopg.errors.DuplicateDatabase):
        conn.execute(f'CREATE DATABASE "{database}"')

    try:
        yield
    finally:
        conn.execute(f'DROP DATABASE "{database}"')
        conn.close()


@pytest.fixture(autouse=True)
def _register_default_connection() -> Generator[None, None, None]:
    init_default_containers()
    connection_mng = Container.managers.get(ConnectionManager)
    test_db_dsn = os.getenv('TEST_DB_DSN', 'postgres://postgres:example@localhost:5432/')

    with create_database(test_db_dsn, 'customers'):
        connection_mng.register_connection_pool(
            DefaultConnectionPool(PostgresConnection, dsn=f'{test_db_dsn}customers'),
        )

        Container.planners.get(SchemaCommandPlanner).plan_schema_command(
            SchemaCommand(
                mutations=[
                    RegisterSchema(
                        schema=Schema(
                            name='customers',
                            version=Version.LATEST,
                            properties=[
                                PropertySchema(
                                    name='id',
                                    type=int,
                                    required=True,
                                ),
                                PropertySchema(
                                    name='age',
                                    type=int,
                                    required=True,
                                ),
                                PropertySchema(
                                    name='first_name',
                                    type=str,
                                    required=False,
                                ),
                                PropertySchema(
                                    name='last_name',
                                    type=str,
                                    required=False,
                                ),
                                PropertySchema(
                                    name='country',
                                    type=str,
                                    required=False,
                                ),
                            ],
                            constraints=[],
                            indexes=[],
                        )
                    ),
                    RegisterSchema(
                        schema=Schema(
                            name='orders',
                            version=Version.LATEST,
                            properties=[
                                PropertySchema(
                                    name='id',
                                    type=int,
                                    required=True,
                                ),
                                PropertySchema(
                                    name='customer_id',
                                    type=int,
                                    required=True,
                                ),
                                PropertySchema(
                                    name='amount',
                                    type=int,
                                    required=False,
                                ),
                                PropertySchema(
                                    name='item',
                                    type=str,
                                    required=False,
                                ),
                            ],
                            constraints=[],
                            indexes=[],
                        )
                    ),
                ],
            ),
        ).execute(transaction_id=None, lock_id=None)

        Container.planners.get(DataCommandPlanner).plan_data_command(
            DataCommand(
                lock_id=None,
                transaction_id=None,
                mutations=[
                    InsertData(
                        schema=SchemaReference(name='customers', version=Version.LATEST),
                        data=[
                            Data(
                                data={
                                    'id': 1,
                                    'age': 31,
                                    'first_name': 'John',
                                    'last_name': 'Doe',
                                    'country': 'USA',
                                },
                            ),
                            Data(
                                data={
                                    'id': 2,
                                    'age': 22,
                                    'first_name': 'Robert',
                                    'last_name': 'Luna',
                                    'country': 'USA',
                                },
                            ),
                            Data(
                                data={
                                    'id': 3,
                                    'age': 22,
                                    'first_name': 'David',
                                    'last_name': 'Robinson',
                                    'country': 'UK',
                                },
                            ),
                            Data(
                                data={
                                    'id': 4,
                                    'age': 25,
                                    'first_name': 'John',
                                    'last_name': 'Reinhardt',
                                    'country': 'USA',
                                },
                            ),
                            Data(
                                data={
                                    'id': 5,
                                    'age': 25,
                                    'first_name': 'Betty',
                                    'last_name': 'Doe',
                                    'country': 'USA',
                                },
                            ),
                        ],
                    ),
                    InsertData(
                        schema=SchemaReference(name='orders', version=Version.LATEST),
                        data=[
                            Data(
                                data={
                                    'id': 1,
                                    'customer_id': 4,
                                    'amount': 400,
                                    'item': 'Keyboard',
                                },
                            ),
                            Data(
                                data={
                                    'id': 2,
                                    'customer_id': 4,
                                    'amount': 300,
                                    'item': 'Mouse',
                                },
                            ),
                            Data(
                                data={
                                    'id': 3,
                                    'customer_id': 3,
                                    'amount': 12000,
                                    'item': 'Monitor',
                                },
                            ),
                            Data(
                                data={
                                    'id': 4,
                                    'customer_id': 1,
                                    'amount': 400,
                                    'item': 'Keyboard',
                                },
                            ),
                            Data(
                                data={
                                    'id': 5,
                                    'customer_id': 2,
                                    'amount': 250,
                                    'item': 'Mousepad',
                                },
                            ),
                            Data(
                                data={
                                    'id': 6,
                                    'customer_id': 6,
                                    'amount': 250,
                                    'item': 'Mousepad',
                                },
                            ),
                        ],
                    ),
                ],
            )
        ).execute(transaction_id=None, lock_id=None)

        with create_database(test_db_dsn, 'shippings'):
            connection_mng.register_connection_pool(
                DefaultConnectionPool(PostgresConnection, dsn=f'{test_db_dsn}shippings'),
                schema_name='shippings',
            )

            Container.planners.get(SchemaCommandPlanner).plan_schema_command(
                SchemaCommand(
                    mutations=[
                        RegisterSchema(
                            schema=Schema(
                                name='shippings',
                                version=Version.LATEST,
                                properties=[
                                    PropertySchema(
                                        name='id',
                                        type=int,
                                        required=True,
                                    ),
                                    PropertySchema(
                                        name='customer_id',
                                        type=int,
                                        required=True,
                                    ),
                                    PropertySchema(
                                        name='status',
                                        type=str,
                                        required=False,
                                    ),
                                ],
                                constraints=[],
                                indexes=[],
                            )
                        ),
                    ],
                ),
            ).execute(transaction_id=None, lock_id=None)

            Container.planners.get(DataCommandPlanner).plan_data_command(
                DataCommand(
                    lock_id=None,
                    transaction_id=None,
                    mutations=[
                        InsertData(
                            schema=SchemaReference(name='shippings', version=Version.LATEST),
                            data=[
                                Data(data={'id': 1, 'customer_id': 2, 'status': 'Pending'}),
                                Data(data={'id': 2, 'customer_id': 4, 'status': 'Pending'}),
                                Data(data={'id': 3, 'customer_id': 3, 'status': 'Delivered'}),
                                Data(data={'id': 4, 'customer_id': 5, 'status': 'Pending'}),
                                Data(data={'id': 5, 'customer_id': 1, 'status': 'Delivered'}),
                                Data(data={'id': 6, 'customer_id': 6, 'status': 'Delivered'}),
                            ],
                        ),
                    ],
                )
            ).execute(transaction_id=None, lock_id=None)

            try:
                yield
            finally:
                connection_mng.disconnect_all()


def test_query_execute_query_to_single_model() -> None:
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
    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    assert plan.final_task is None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.tasks[-1].result
    assert [item.data for item in result] == [
        {'id': 1, 'first_name': 'John'},
        {'id': 2, 'first_name': 'Robert'},
        {'id': 3, 'first_name': 'David'},
        {'id': 4, 'first_name': 'John'},
        {'id': 5, 'first_name': 'Betty'},
    ]


def test_query_execute_query_aggregation() -> None:
    query = QueryStatement(
        aggregations=[
            AggregationQuery(
                expression=Sum(
                    field=FieldReference(field=Field(name='amount'), table_name='o'),
                ),
                alias='total_amount',
            ),
        ],
        table=SchemaReference(name='orders', alias='o', version=Version.LATEST),
    )
    planner: DataQueryPlanner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    assert plan.final_task is None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.tasks[-1].result
    assert [item.data for item in result] == [
        {'total_amount': 13600},
    ]


def test_query_execute_query_to_single_connection() -> None:
    query = QueryStatement(
        only=[
            FieldReference(field=Field(name='id'), table_name='c'),
            FieldReference(field=Field(name='first_name'), table_name='c'),
            FieldReference(field=Field(name='amount'), table_name='o'),
        ],
        table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
        joins=[
            JoinQuery(
                table=SchemaReference(name='orders', alias='o', version=Version.LATEST),
                on=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='customer_id'), table_name='o')
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
                field=FieldReference(field=Field(name='id'), table_name='o'),
                direction=OrderDirection.ASC,
            ),
        ],
    )
    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    assert plan.final_task is None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.tasks[-1].result
    assert [item.data for item in result] == [
        {'id': 1, 'first_name': 'John', 'amount': 400},
        {'id': 2, 'first_name': 'Robert', 'amount': 250},
        {'id': 3, 'first_name': 'David', 'amount': 12000},
        {'id': 4, 'first_name': 'John', 'amount': 400},
        {'id': 4, 'first_name': 'John', 'amount': 300},
    ]


def test_query_execute_query_to_single_connection_fail_due_to_duplicated_selections() -> None:
    query = QueryStatement(
        table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
        joins=[
            JoinQuery(
                table=SchemaReference(name='orders', alias='o', version=Version.LATEST),
                on=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='customer_id'), table_name='o')
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
                field=FieldReference(field=Field(name='id'), table_name='o'),
                direction=OrderDirection.ASC,
            ),
        ],
    )
    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    assert plan.final_task is None

    with pytest.raises(ValueError, match=r'Column name id is duplicated'):
        plan.execute(transaction_id=None, lock_id=None)


def test_query_execute_query_to_single_connection_subquery_aggr() -> None:
    query = QueryStatement(
        only=[
            FieldReferenceAliased(alias='customer_id', field=Field(name='id'), table_name='c'),
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
                                left=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='customer_id'), table_name='o')
                                ),
                                lookup=FieldLookup.EQ,
                                right=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='id'), table_name='c')
                                ),
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

    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    assert plan.final_task is None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.tasks[-1].result
    assert [item.data for item in result] == [
        {'customer_id': 1, 'total_amount': 400},
        {'customer_id': 2, 'total_amount': 250},
        {'customer_id': 3, 'total_amount': 12000},
        {'customer_id': 4, 'total_amount': 700},
        {'customer_id': 5, 'total_amount': None},
    ]


def test_query_execute_query_to_multiple_connections() -> None:
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

    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    assert plan.final_task is not None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.final_task.result

    assert [item.data for item in result] == [
        {'id': 1, 'first_name': 'John', 'status': 'Delivered'},
        {'id': 2, 'first_name': 'Robert', 'status': 'Pending'},
        {'id': 3, 'first_name': 'David', 'status': 'Delivered'},
        {'id': 4, 'first_name': 'John', 'status': 'Pending'},
        {'id': 5, 'first_name': 'Betty', 'status': 'Pending'},
    ]


def test_query_execute_query_with_subquery_in_from_to_multiple_connections() -> None:
    query = QueryStatement(
        only=[
            FieldReference(field=Field(name='id'), table_name='c'),
            FieldReference(field=Field(name='first_name'), table_name='c'),
            FieldReference(field=Field(name='status'), table_name='s'),
        ],
        table=SubQueryStatement(
            alias='c',
            query=QueryStatement(table=SchemaReference(name='customers', alias='c', version=Version.LATEST)),
        ),
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

    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    assert plan.final_task is not None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.final_task.result

    assert [item.data for item in result] == [
        {'id': 1, 'first_name': 'John', 'status': 'Delivered'},
        {'id': 2, 'first_name': 'Robert', 'status': 'Pending'},
        {'id': 3, 'first_name': 'David', 'status': 'Delivered'},
        {'id': 4, 'first_name': 'John', 'status': 'Pending'},
        {'id': 5, 'first_name': 'Betty', 'status': 'Pending'},
    ]


def test_query_execute_query_with_subquery_in_join_to_multiple_connections() -> None:
    query = QueryStatement(
        only=[
            FieldReference(field=Field(name='id'), table_name='c'),
            FieldReference(field=Field(name='first_name'), table_name='c'),
            FieldReference(field=Field(name='status'), table_name='s'),
        ],
        table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
        joins=[
            JoinQuery(
                table=SubQueryStatement(
                    alias='s',
                    query=QueryStatement(table=SchemaReference(name='shippings', version=Version.LATEST)),
                ),
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

    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    assert plan.final_task is not None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.final_task.result

    assert [item.data for item in result] == [
        {'id': 1, 'first_name': 'John', 'status': 'Delivered'},
        {'id': 2, 'first_name': 'Robert', 'status': 'Pending'},
        {'id': 3, 'first_name': 'David', 'status': 'Delivered'},
        {'id': 4, 'first_name': 'John', 'status': 'Pending'},
        {'id': 5, 'first_name': 'Betty', 'status': 'Pending'},
    ]


def test_query_execute_query_with_subquery_annotation_to_multiple_connections() -> None:
    query = QueryStatement(
        only=[
            FieldReferenceAliased(alias='customer_id', field=Field(name='id'), table_name='s'),
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
                                left=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='customer_id'), table_name='o')
                                ),
                                lookup=FieldLookup.EQ,
                                right=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='customer_id'), table_name='s')
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ],
        table=SchemaReference(name='shippings', alias='s', version=Version.LATEST),
        order_by=[
            OrderByQuery(
                field=FieldReference(field=Field(name='customer_id'), table_name='s'),
                direction=OrderDirection.ASC,
            ),
        ],
    )

    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    assert plan.final_task is not None

    with pytest.raises(RuntimeError, match='PolarsFinalQueryExecutor does not support subquery annotations'):
        plan.execute(transaction_id=None, lock_id=None)


def test_query_execute_distinct() -> None:
    query = QueryStatement(
        only=[
            FieldReference(field=Field(name='first_name'), table_name='c'),
        ],
        distinct=True,
        table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
        order_by=[
            OrderByQuery(
                field=FieldReference(field=Field(name='first_name'), table_name='c'),
                direction=OrderDirection.ASC,
            ),
        ],
    )

    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    assert plan.final_task is None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.tasks[-1].result
    assert [item.data for item in result] == [
        {'first_name': 'Betty'},
        {'first_name': 'David'},
        {'first_name': 'John'},
        {'first_name': 'Robert'},
    ]


def test_query_execute_distinct_multiple_fields() -> None:
    query = QueryStatement(
        only=[
            FieldReference(field=Field(name='first_name'), table_name='c'),
            FieldReference(field=Field(name='last_name'), table_name='c'),
        ],
        distinct=True,
        table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
        order_by=[
            OrderByQuery(
                field=FieldReference(field=Field(name='first_name'), table_name='c'),
                direction=OrderDirection.ASC,
            ),
        ],
    )

    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    assert plan.final_task is None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.tasks[-1].result
    assert [item.data for item in result] == [
        {'first_name': 'Betty', 'last_name': 'Doe'},
        {'first_name': 'David', 'last_name': 'Robinson'},
        {'first_name': 'John', 'last_name': 'Doe'},
        {'first_name': 'John', 'last_name': 'Reinhardt'},
        {'first_name': 'Robert', 'last_name': 'Luna'},
    ]


def test_query_execute_distinct_on_single_field() -> None:
    query = QueryStatement(
        only=[
            FieldReference(field=Field(name='first_name'), table_name='c'),
        ],
        distinct=[
            FieldReference(field=Field(name='first_name'), table_name='c'),
        ],
        table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
        order_by=[
            OrderByQuery(
                field=FieldReference(field=Field(name='first_name'), table_name='c'),
                direction=OrderDirection.ASC,
            ),
        ],
    )

    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    assert plan.final_task is None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.tasks[-1].result
    assert [item.data for item in result] == [
        {'first_name': 'Betty'},
        {'first_name': 'David'},
        {'first_name': 'John'},
        {'first_name': 'Robert'},
    ]


def test_query_execute_distinct_on_single_field_multiple_selected() -> None:
    query = QueryStatement(
        only=[
            FieldReference(field=Field(name='first_name'), table_name='c'),
            FieldReference(field=Field(name='last_name'), table_name='c'),
        ],
        distinct=[
            FieldReference(field=Field(name='first_name'), table_name='c'),
        ],
        table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
        order_by=[
            OrderByQuery(
                field=FieldReference(field=Field(name='first_name'), table_name='c'),
                direction=OrderDirection.ASC,
            ),
        ],
    )

    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    assert plan.final_task is None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.tasks[-1].result
    assert [item.data for item in result] == [
        {'first_name': 'Betty', 'last_name': 'Doe'},
        {'first_name': 'David', 'last_name': 'Robinson'},
        {'first_name': 'John', 'last_name': 'Doe'},
        {'first_name': 'Robert', 'last_name': 'Luna'},
    ]


def test_query_execute_distinct_on_multiple() -> None:
    query = QueryStatement(
        only=[
            FieldReference(field=Field(name='first_name'), table_name='c'),
            FieldReference(field=Field(name='last_name'), table_name='c'),
        ],
        distinct=[
            FieldReference(field=Field(name='first_name'), table_name='c'),
            FieldReference(field=Field(name='last_name'), table_name='c'),
        ],
        table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
        order_by=[
            OrderByQuery(
                field=FieldReference(field=Field(name='first_name'), table_name='c'),
                direction=OrderDirection.ASC,
            ),
        ],
    )

    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    assert plan.final_task is None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.tasks[-1].result
    assert [item.data for item in result] == [
        {'first_name': 'Betty', 'last_name': 'Doe'},
        {'first_name': 'David', 'last_name': 'Robinson'},
        {'first_name': 'John', 'last_name': 'Doe'},
        {'first_name': 'John', 'last_name': 'Reinhardt'},
        {'first_name': 'Robert', 'last_name': 'Luna'},
    ]
