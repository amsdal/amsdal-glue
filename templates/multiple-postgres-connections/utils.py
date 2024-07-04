from amsdal_glue_core.common.data_models.schema import Schema

from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.services.commands import SchemaCommandService
from amsdal_glue_core.containers import Container
from amsdal_glue_core.common.services.managers.connection import ConnectionManager
from amsdal_glue.connections.connection_pool import DefaultConnectionPool
from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection

from amsdal_glue_core.common.operations.queries import SchemaQueryOperation
from amsdal_glue_core.common.services.queries import SchemaQueryService

from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.services.commands import DataCommandService

from amsdal_glue_core.common.data_models.data import Data

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.services.queries import DataQueryService
from amsdal_glue.initialize import init_default_containers


def register_connections() -> None:
    existing_db_pool = DefaultConnectionPool(
        PostgresConnection,
        dsn='postgres://db_user:db_password@localhost:5432/db_name_1',
    )
    new_db_pool = DefaultConnectionPool(
        PostgresConnection,
        dsn='postgres://db_user:db_password@localhost:5433/db_name_2',
    )

    connection_mng = Container.managers.get(ConnectionManager)
    connection_mng.register_connection_pool(existing_db_pool)
    connection_mng.register_connection_pool(new_db_pool, schema_name='shipping')


def create_schema_in_new_db() -> None:
    shipping_schema = Schema(
        name='shipping',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='shipping_id',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='status',
                type=str,
                required=True,
            ),
            PropertySchema(
                name='customer_id',
                type=int,
                required=True,
            ),
        ],
        constraints=[
            PrimaryKeyConstraint(name='pk_shipping', fields=['shipping_id']),
        ],
    )

    service = Container.services.get(SchemaCommandService)
    result = service.execute(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=shipping_schema),
            ],
        ),
    )

    assert result.success is True, result.message


def fetch_schemas() -> list[Schema]:
    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        SchemaQueryOperation(filters=None),
    )
    assert result.success is True, result.message
    assert result.schemas is not None

    return result.schemas


def create_new_records() -> None:
    service = Container.services.get(DataCommandService)
    result = service.execute(
        command=DataCommand(
            mutations=[
                InsertData(
                    schema=SchemaReference(name='shipping', version=Version.LATEST),
                    data=[
                        Data(data={'shipping_id': 1, 'status': 'Pending', 'customer_id': 2}),
                        Data(data={'shipping_id': 2, 'status': 'Pending', 'customer_id': 4}),
                        Data(data={'shipping_id': 3, 'status': 'Delivered', 'customer_id': 3}),
                        Data(data={'shipping_id': 4, 'status': 'Pending', 'customer_id': 5}),
                        Data(data={'shipping_id': 5, 'status': 'Delivered', 'customer_id': 1}),
                    ],
                ),
            ],
        ),
    )

    assert result.success is True


def fetch_customers_and_their_shipping_status() -> list[Data]:
    query = QueryStatement(
        only=[
            FieldReference(field=Field(name='customer_id'), table_name='c'),
            FieldReference(field=Field(name='first_name'), table_name='c'),
            FieldReference(field=Field(name='status'), table_name='s'),
        ],
        table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
        joins=[
            JoinQuery(
                table=SchemaReference(name='shipping', alias='s', version=Version.LATEST),
                on=Conditions(
                    Condition(
                        field=FieldReference(field=Field(name='customer_id'), table_name='s'),
                        lookup=FieldLookup.EQ,
                        value=FieldReference(field=Field(name='customer_id'), table_name='c'),
                    ),
                ),
                join_type=JoinType.INNER,
            ),
        ],
        order_by=[
            OrderByQuery(
                field=FieldReference(field=Field(name='customer_id'), table_name='c'),
                direction=OrderDirection.ASC,
            ),
            OrderByQuery(
                field=FieldReference(field=Field(name='shipping_id'), table_name='s'),
                direction=OrderDirection.ASC,
            ),
        ],
    )

    service = Container.services.get(DataQueryService)
    data_result = service.execute(
        query_op=DataQueryOperation(
            query=query,
        ),
    )
    assert data_result.success is True, data_result.message

    return data_result.data
