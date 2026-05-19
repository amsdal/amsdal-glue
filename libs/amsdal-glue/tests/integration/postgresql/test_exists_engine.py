# mypy: disable-error-code="type-abstract"
import os
import uuid
from collections.abc import Generator
from contextlib import contextmanager
from contextlib import suppress
from pathlib import Path

import psycopg
import pytest
from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from amsdal_glue_core.commands.planner.data_command_planner import DataCommandPlanner
from amsdal_glue_core.commands.planner.schema_command_planner import SchemaCommandPlanner
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.exists import Exists
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
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
    db_name = f'test_{uuid.uuid4().hex}'

    with create_database(test_db_dsn, db_name):
        connection_mng.register_connection_pool(
            DefaultConnectionPool(PostgresConnection, dsn=f'{test_db_dsn}{db_name}'),
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

        try:
            yield
        finally:
            connection_mng.disconnect_all()


def _correlated_orders_subquery(min_amount: int) -> QueryStatement:
    leaves: list[Condition] = [
        Condition(
            left=FieldReferenceExpression(
                field_reference=FieldReference(
                    field=Field(name='customer_id'),
                    table_name='o',
                )
            ),
            lookup=FieldLookup.EQ,
            right=FieldReferenceExpression(
                field_reference=FieldReference(
                    field=Field(name='id'),
                    table_name='c',
                )
            ),
        ),
    ]
    if min_amount > 0:
        leaves.append(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(
                        field=Field(name='amount'),
                        table_name='o',
                    )
                ),
                lookup=FieldLookup.GT,
                right=Value(value=min_amount),
            )
        )

    return QueryStatement(
        only=[FieldReference(field=Field(name='1'), table_name='')],
        table=SchemaReference(name='orders', alias='o', version=Version.LATEST),
        where=Conditions(*leaves),
    )


def test_not_exists_returns_customers_without_any_orders() -> None:
    query = QueryStatement(
        only=[FieldReference(field=Field(name='id'), table_name='c')],
        table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
        where=Conditions(Exists(query=_correlated_orders_subquery(min_amount=0), negated=True)),
        order_by=[
            OrderByQuery(
                field=FieldReference(field=Field(name='id'), table_name='c'),
                direction=OrderDirection.ASC,
            )
        ],
    )
    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    plan.execute(transaction_id=None, lock_id=None)

    result = plan.tasks[-1].result

    assert [item.data for item in result] == [{'id': 5}]


def test_exists_returns_customers_with_any_order() -> None:
    query = QueryStatement(
        only=[FieldReference(field=Field(name='id'), table_name='c')],
        table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
        where=Conditions(Exists(query=_correlated_orders_subquery(min_amount=0))),
        order_by=[
            OrderByQuery(
                field=FieldReference(field=Field(name='id'), table_name='c'),
                direction=OrderDirection.ASC,
            )
        ],
    )
    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    plan.execute(transaction_id=None, lock_id=None)

    result = plan.tasks[-1].result

    assert [item.data for item in result] == [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}]


def test_exists_with_correlation_and_amount_threshold_returns_customer_three() -> None:
    """Only customer 3 has an order with amount > 5000 (order id=3, amount=12000)."""
    query = QueryStatement(
        only=[FieldReference(field=Field(name='id'), table_name='c')],
        table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
        where=Conditions(Exists(query=_correlated_orders_subquery(min_amount=5000))),
        order_by=[
            OrderByQuery(
                field=FieldReference(field=Field(name='id'), table_name='c'),
                direction=OrderDirection.ASC,
            )
        ],
    )
    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    plan.execute(transaction_id=None, lock_id=None)

    result = plan.tasks[-1].result

    assert [item.data for item in result] == [{'id': 3}]
