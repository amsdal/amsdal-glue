import amsdal_glue
from amsdal_glue import Condition
from amsdal_glue import Conditions
from amsdal_glue import Data
from amsdal_glue import Field
from amsdal_glue import FieldLookup
from amsdal_glue import FieldReference
from amsdal_glue import JoinQuery
from amsdal_glue import JoinType
from amsdal_glue import OrderByQuery
from amsdal_glue import OrderDirection
from amsdal_glue import PrimaryKeyConstraint
from amsdal_glue import PropertySchema
from amsdal_glue import QueryStatement
from amsdal_glue import Schema
from amsdal_glue import SchemaReference
from amsdal_glue import Version


def register_connections() -> None:
    existing_db_pool = amsdal_glue.DefaultConnectionPool(
        amsdal_glue.PostgresConnection,
        dsn="postgres://db_user:db_password@localhost:5432/db_name_1",
    )
    new_db_pool = amsdal_glue.DefaultConnectionPool(
        amsdal_glue.PostgresConnection,
        dsn="postgres://db_user:db_password@localhost:5433/db_name_2",
    )

    connection_mng = amsdal_glue.Container.managers.get(amsdal_glue.ConnectionManager)
    connection_mng.register_connection_pool(existing_db_pool)
    connection_mng.register_connection_pool(new_db_pool, schema_name="shipping")


def create_schema_in_new_db() -> None:
    shipping_schema = Schema(
        name="shipping",
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name="shipping_id",
                type=int,
                required=True,
            ),
            PropertySchema(
                name="status",
                type=str,
                required=True,
            ),
            PropertySchema(
                name="customer_id",
                type=int,
                required=True,
            ),
        ],
        constraints=[
            PrimaryKeyConstraint(name="pk_shipping", fields=["shipping_id"]),
        ],
    )

    service = amsdal_glue.Container.services.get(amsdal_glue.SchemaCommandService)
    result = service.execute(
        amsdal_glue.SchemaCommand(
            mutations=[
                amsdal_glue.RegisterSchema(schema=shipping_schema),
            ],
        ),
    )

    assert result.success is True, result.message


def fetch_schemas() -> list[Schema]:
    query_service = amsdal_glue.Container.services.get(amsdal_glue.SchemaQueryService)
    result = query_service.execute(
        amsdal_glue.SchemaQueryOperation(filters=None),
    )
    assert result.success is True, result.message
    assert result.schemas is not None

    return result.schemas


def create_new_records() -> None:
    service = amsdal_glue.Container.services.get(amsdal_glue.DataCommandService)
    result = service.execute(
        command=amsdal_glue.DataCommand(
            mutations=[
                amsdal_glue.InsertData(
                    schema=SchemaReference(name="shipping", version=Version.LATEST),
                    data=[
                        Data(
                            data={
                                "shipping_id": 1,
                                "status": "Pending",
                                "customer_id": 2,
                            }
                        ),
                        Data(
                            data={
                                "shipping_id": 2,
                                "status": "Pending",
                                "customer_id": 4,
                            }
                        ),
                        Data(
                            data={
                                "shipping_id": 3,
                                "status": "Delivered",
                                "customer_id": 3,
                            }
                        ),
                        Data(
                            data={
                                "shipping_id": 4,
                                "status": "Pending",
                                "customer_id": 5,
                            }
                        ),
                        Data(
                            data={
                                "shipping_id": 5,
                                "status": "Delivered",
                                "customer_id": 1,
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

    service = amsdal_glue.Container.services.get(amsdal_glue.DataQueryService)
    data_result = service.execute(
        query_op=amsdal_glue.DataQueryOperation(
            query=query,
        ),
    )
    assert data_result.success is True, data_result.message

    return data_result.data
