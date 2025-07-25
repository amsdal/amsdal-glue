# mypy: disable-error-code="type-abstract,attr-defined,return-value,arg-type,operator"
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
from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.annotation import ExpressionAnnotation
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
from amsdal_glue_core.common.data_models.schema import VectorSchemaModel
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.data_models.vector import Vector
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.expressions.vector import CosineDistanceExpression
from amsdal_glue_core.common.expressions.vector import InnerProductExpression
from amsdal_glue_core.common.expressions.vector import L1DistanceExpression
from amsdal_glue_core.common.expressions.vector import L2DistanceExpression
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

    db_conn = psycopg.connect(f'{dsn}{database}', autocommit=True)
    db_conn.execute('CREATE EXTENSION IF NOT EXISTS vector;')
    db_conn.close()

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
                            name='vector_schema',
                            version=Version.LATEST,
                            properties=[
                                PropertySchema(
                                    name='id',
                                    type=int,
                                    required=True,
                                ),
                                PropertySchema(
                                    name='vector',
                                    type=VectorSchemaModel(dimensions=3),
                                    required=True,
                                ),
                            ],
                            constraints=[],
                            indexes=[],
                        )
                    ),
                    RegisterSchema(
                        schema=Schema(
                            name='binary_vector_schema',
                            version=Version.LATEST,
                            properties=[
                                PropertySchema(
                                    name='id',
                                    type=int,
                                    required=True,
                                ),
                                PropertySchema(
                                    name='vector',
                                    type=VectorSchemaModel(dimensions=2),
                                    required=True,
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
                        schema=SchemaReference(name='vector_schema', version=Version.LATEST),
                        data=[
                            Data(
                                data={'vector': '[1,2,3]', 'id': 1},
                            ),
                            Data(
                                data={'vector': Vector(values=[4, 5, 6]), 'id': 2},
                            ),
                            Data(
                                data={'vector': Vector(values=[7, 8, 9]), 'id': 3},
                            ),
                        ],
                    ),
                    InsertData(
                        schema=SchemaReference(name='binary_vector_schema', version=Version.LATEST),
                        data=[
                            Data(
                                data={'vector': Vector(values=[1, 2]), 'id': 1},
                            ),
                            Data(
                                data={'vector': Vector(values=[4, 5]), 'id': 2},
                            ),
                            Data(
                                data={'vector': Vector(values=[7, 8]), 'id': 3},
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


def test_query_execute_vector_operations() -> None:
    query = QueryStatement(
        only=[
            FieldReference(field=Field(name='id'), table_name='v'),
            FieldReference(field=Field(name='vector'), table_name='v'),
        ],
        table=SchemaReference(name='vector_schema', alias='v', version=Version.LATEST),
    )

    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    assert plan.final_task is None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.tasks[-1].result
    assert [item.data for item in result] == [
        {
            'id': 1,
            'vector': [1, 2, 3],
        },
        {
            'id': 2,
            'vector': [4, 5, 6],
        },
        {
            'id': 3,
            'vector': [7, 8, 9],
        },
    ]


@pytest.mark.parametrize(
    'distance_expression,expected1,expected2,expected3,value_to_filter',
    [
        (
            L2DistanceExpression,
            5.385164807134504,
            1.4142135623730951,
            5.385164807134504,
            5,
        ),
        (
            CosineDistanceExpression,
            0.07417990022744847,
            0.013072457560346584,
            0.005167993252386149,
            0.01,
        ),
        (
            L1DistanceExpression,
            9.0,
            2.0,
            9.0,
            3,
        ),
    ],
)
def test_query_execute_vector_operations_with_annotations(
    distance_expression,
    expected1: float,
    expected2: float,
    expected3: float,
    value_to_filter: float,
) -> None:
    _expected_result = [
        {
            'distance_to_self': 0.0,
            'distance_to_value': expected1,
            'id': 1,
            'vector': [1, 2, 3],
        },
        {
            'distance_to_self': 0.0,
            'distance_to_value': expected2,
            'id': 2,
            'vector': [4, 5, 6],
        },
        {
            'distance_to_self': 0.0,
            'distance_to_value': expected3,
            'id': 3,
            'vector': [7, 8, 9],
        },
    ]
    query = QueryStatement(
        only=[
            FieldReference(field=Field(name='id'), table_name='v'),
            FieldReference(field=Field(name='vector'), table_name='v'),
        ],
        table=SchemaReference(name='vector_schema', alias='v', version=Version.LATEST),
        annotations=[
            AnnotationQuery(
                value=ExpressionAnnotation(
                    alias='distance_to_self',
                    expression=distance_expression(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='vector'), table_name='v')
                        ),
                        right=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='vector'), table_name='v')
                        ),
                    ),
                ),
            ),
            AnnotationQuery(
                value=ExpressionAnnotation(
                    alias='distance_to_value',
                    expression=distance_expression(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='vector'), table_name='v')
                        ),
                        right=Value(value=Vector(values=[5, 5, 5])),
                    ),
                ),
            ),
        ],
    )

    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    assert plan.final_task is None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.tasks[-1].result
    assert [item.data for item in result] == _expected_result

    outer_query = QueryStatement(
        table=SubQueryStatement(
            query=query,
            alias='vv',
        ),
        only=[
            FieldReference(field=Field(name='id'), table_name='vv'),
            FieldReference(field=Field(name='vector'), table_name='vv'),
            FieldReference(field=Field(name='distance_to_self'), table_name='vv'),
            FieldReference(field=Field(name='distance_to_value'), table_name='vv'),
        ],
        order_by=[
            OrderByQuery(
                field=FieldReference(field=Field(name='distance_to_value'), table_name='vv'),
                direction=OrderDirection.ASC,
            ),
            OrderByQuery(
                field=FieldReference(field=Field(name='id'), table_name='vv'),
                direction=OrderDirection.ASC,
            ),
        ],
    )
    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(outer_query)
    assert plan.final_task is None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.tasks[-1].result
    assert [item.data for item in result] == sorted(_expected_result, key=lambda x: x['distance_to_value'])

    outer_query.where = Conditions(
        Condition(
            left=FieldReferenceExpression(
                field_reference=FieldReference(field=Field(name='distance_to_value'), table_name='vv')
            ),
            lookup=FieldLookup.GT,
            right=Value(value=value_to_filter),
        ),
    )

    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(outer_query)
    assert plan.final_task is None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.tasks[-1].result
    assert [item.data for item in result] == [
        v
        for v in sorted(_expected_result, key=lambda x: x['distance_to_value'])
        if v['distance_to_value'] > value_to_filter
    ]

    outer_query.where = Conditions(
        Condition(
            left=FieldReferenceExpression(
                field_reference=FieldReference(field=Field(name='distance_to_value'), table_name='vv')
            ),
            lookup=FieldLookup.LT,
            right=Value(value=value_to_filter),
        ),
    )

    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(outer_query)
    assert plan.final_task is None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.tasks[-1].result
    assert [item.data for item in result] == [
        v
        for v in sorted(_expected_result, key=lambda x: x['distance_to_value'])
        if v['distance_to_value'] < value_to_filter
    ]


def test_query_execute_vector_operations_with_annotations_inner_distance() -> None:
    filter_value = -50
    _expected_result = [
        {
            'distance_to_self': -14,
            'distance_to_value': -30,
            'id': 1,
            'vector': [1, 2, 3],
        },
        {
            'distance_to_self': -77,
            'distance_to_value': -75,
            'id': 2,
            'vector': [4, 5, 6],
        },
        {
            'distance_to_self': -194,
            'distance_to_value': -120,
            'id': 3,
            'vector': [7, 8, 9],
        },
    ]
    query = QueryStatement(
        only=[
            FieldReference(field=Field(name='id'), table_name='v'),
            FieldReference(field=Field(name='vector'), table_name='v'),
        ],
        table=SchemaReference(name='vector_schema', alias='v', version=Version.LATEST),
        annotations=[
            AnnotationQuery(
                value=ExpressionAnnotation(
                    alias='distance_to_self',
                    expression=InnerProductExpression(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='vector'), table_name='v')
                        ),
                        right=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='vector'), table_name='v')
                        ),
                    ),
                ),
            ),
            AnnotationQuery(
                value=ExpressionAnnotation(
                    alias='distance_to_value',
                    expression=InnerProductExpression(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='vector'), table_name='v')
                        ),
                        right=Value(value=Vector(values=[5, 5, 5])),
                    ),
                ),
            ),
        ],
    )

    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    assert plan.final_task is None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.tasks[-1].result
    assert [item.data for item in result] == _expected_result

    outer_query = QueryStatement(
        table=SubQueryStatement(
            query=query,
            alias='vv',
        ),
        only=[
            FieldReference(field=Field(name='id'), table_name='vv'),
            FieldReference(field=Field(name='vector'), table_name='vv'),
            FieldReference(field=Field(name='distance_to_self'), table_name='vv'),
            FieldReference(field=Field(name='distance_to_value'), table_name='vv'),
        ],
        order_by=[
            OrderByQuery(
                field=FieldReference(field=Field(name='distance_to_value'), table_name='vv'),
                direction=OrderDirection.ASC,
            ),
            OrderByQuery(
                field=FieldReference(field=Field(name='id'), table_name='vv'),
                direction=OrderDirection.ASC,
            ),
        ],
    )
    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(outer_query)
    assert plan.final_task is None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.tasks[-1].result
    assert [item.data for item in result] == sorted(_expected_result, key=lambda x: x['distance_to_value'])

    outer_query.where = Conditions(
        Condition(
            left=FieldReferenceExpression(
                field_reference=FieldReference(field=Field(name='distance_to_value'), table_name='vv')
            ),
            lookup=FieldLookup.GT,
            right=Value(value=filter_value),
        ),
    )

    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(outer_query)
    assert plan.final_task is None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.tasks[-1].result
    assert [item.data for item in result] == [
        v
        for v in sorted(_expected_result, key=lambda x: x['distance_to_value'])
        if v['distance_to_value'] > filter_value
    ]

    outer_query.where = Conditions(
        Condition(
            left=FieldReferenceExpression(
                field_reference=FieldReference(field=Field(name='distance_to_value'), table_name='vv')
            ),
            lookup=FieldLookup.LT,
            right=Value(value=filter_value),
        ),
    )

    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(outer_query)
    assert plan.final_task is None

    plan.execute(transaction_id=None, lock_id=None)
    result = plan.tasks[-1].result
    assert [item.data for item in result] == [
        v
        for v in sorted(_expected_result, key=lambda x: x['distance_to_value'])
        if v['distance_to_value'] < filter_value
    ]
