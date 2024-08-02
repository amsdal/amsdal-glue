from amsdal_glue_core.common.data_models.schema import Schema

from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.services.commands import SchemaCommandService
from amsdal_glue_core.containers import Container
from amsdal_glue_core.common.services.managers.connection import ConnectionManager
from amsdal_glue.connections.connection_pool import DefaultConnectionPool


from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.services.commands import DataCommandService

from amsdal_glue_core.common.data_models.data import Data

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_connections.sql.connections.postgres_connection import (
    PostgresConnection,
)
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.services.queries import DataQueryService

from amsdal_glue_sql_parser.parsers.base import SqlParserBase
from amsdal_glue_sql_parser.parsers.sqloxide_parser import SqlOxideParser


def register_connections() -> None:
    customers_db_pool = DefaultConnectionPool(
        PostgresConnection,
        dsn="postgres://db_user:db_password@localhost:5432/db_name_1",
        # autocommit=True,
    )
    orders_db_pool = DefaultConnectionPool(
        PostgresConnection,
        dsn="postgres://db_user:db_password@localhost:5433/db_name_2",
        # autocommit=True,
    )
    connection_mng = Container.managers.get(ConnectionManager)
    connection_mng.register_connection_pool(customers_db_pool, schema_name="customers")
    connection_mng.register_connection_pool(orders_db_pool, schema_name="orders")


def register_parser() -> None:
    Container.services.register(SqlParserBase, SqlOxideParser)


def create_schemas() -> None:
    customers_schema = Schema(
        name="customers",
        version=Version.LATEST,
        properties=[
            PropertySchema(name="id", type=int, required=True),
            PropertySchema(name="first_name", type=str, required=True),
            PropertySchema(name="last_name", type=str, required=True),
        ],
    )
    orders_schema = Schema(
        name="orders",
        version=Version.LATEST,
        properties=[
            PropertySchema(name="id", type=int, required=True),
            PropertySchema(name="customer_id", type=int, required=True),
            PropertySchema(name="product", type=str, required=True),
            PropertySchema(name="price", type=float, required=True),
        ],
    )

    service = Container.services.get(SchemaCommandService)
    result = service.execute(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=customers_schema),
            ],
        ),
    )
    result = service.execute(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=orders_schema),
            ],
        ),
    )

    assert result.success is True, result.message


def create_new_records() -> None:
    service = Container.services.get(DataCommandService)
    result = service.execute(
        command=DataCommand(
            mutations=[
                InsertData(
                    schema=SchemaReference(name="customers", version=Version.LATEST),
                    data=[
                        Data(
                            data={
                                "id": 1,
                                "first_name": "John",
                                "last_name": "Doe",
                            }
                        ),
                        Data(
                            data={
                                "id": 2,
                                "first_name": "Jane",
                                "last_name": "Smith",
                            }
                        ),
                        Data(
                            data={
                                "id": 3,
                                "first_name": "Alice",
                                "last_name": "Johnson",
                            }
                        ),
                        Data(
                            data={
                                "id": 4,
                                "first_name": "Bob",
                                "last_name": "Brown",
                            }
                        ),
                    ],
                ),
                InsertData(
                    schema=SchemaReference(name="orders", version=Version.LATEST),
                    data=[
                        Data(
                            data={
                                "id": 1,
                                "customer_id": 1,
                                "product": "Laptop",
                                "price": 1000.0,
                            }
                        ),
                        Data(
                            data={
                                "id": 2,
                                "customer_id": 2,
                                "product": "Phone",
                                "price": 500.0,
                            }
                        ),
                        Data(
                            data={
                                "id": 3,
                                "customer_id": 3,
                                "product": "Tablet",
                                "price": 800.0,
                            }
                        ),
                        Data(
                            data={
                                "id": 4,
                                "customer_id": 3,
                                "product": "Headphones",
                                "price": 200.0,
                            }
                        ),
                    ],
                ),
            ],
        ),
    )

    assert result.success is True


def fetch_customers_and_their_shipping_status() -> list[Data]:
    query = QueryStatement(
        only=[
            FieldReference(field=Field(name="customer_id"), table_name="c"),
            FieldReference(field=Field(name="first_name"), table_name="c"),
            FieldReference(field=Field(name="status"), table_name="s"),
        ],
        table=SchemaReference(name="customers", alias="c", version=Version.LATEST),
        joins=[
            JoinQuery(
                table=SchemaReference(
                    name="shipping", alias="s", version=Version.LATEST
                ),
                on=Conditions(
                    Condition(
                        field=FieldReference(
                            field=Field(name="customer_id"), table_name="s"
                        ),
                        lookup=FieldLookup.EQ,
                        value=FieldReference(
                            field=Field(name="customer_id"), table_name="c"
                        ),
                    ),
                ),
                join_type=JoinType.INNER,
            ),
        ],
        order_by=[
            OrderByQuery(
                field=FieldReference(field=Field(name="customer_id"), table_name="c"),
                direction=OrderDirection.ASC,
            ),
            OrderByQuery(
                field=FieldReference(field=Field(name="shipping_id"), table_name="s"),
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
