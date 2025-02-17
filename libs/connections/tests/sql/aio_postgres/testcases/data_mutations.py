from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.data import DeleteData
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateData

from amsdal_glue_connections.sql.connections.postgres_connection import AsyncPostgresConnection


async def simple_customer_insert(
    database_connection: AsyncPostgresConnection, namespace: str = ''
) -> list[list[Data] | None]:
    return await database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name='customers', namespace=namespace, version=Version.LATEST),
            data=[
                Data(
                    data={'id': '1', 'name': 'customer'},
                )
            ],
        ),
    ])


async def insert_customers_and_orders(
    database_connection: AsyncPostgresConnection,
    namespace_1: str = '',
    namespace_2: str = '',
) -> list[list[Data] | None]:
    return await database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name='customers', namespace=namespace_1, version=Version.LATEST),
            data=[
                Data(
                    data={'id': '1', 'name': 'customer'},
                )
            ],
        ),
        InsertData(
            schema=SchemaReference(name='customers', namespace=namespace_1, version=Version.LATEST),
            data=[
                Data(
                    data={'id': '2', 'name': 'customer', 'age': 25},
                )
            ],
        ),
        InsertData(
            schema=SchemaReference(name='orders', namespace=namespace_2, version=Version.LATEST),
            data=[
                Data(
                    data={'id': '1', 'customer_id': '1', 'amount': 100},
                )
            ],
        ),
    ])


async def update_two_customers(
    database_connection: AsyncPostgresConnection, namespace: str = ''
) -> list[list[Data] | None]:
    return await database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name='customers', namespace=namespace, version=Version.LATEST),
            data=[
                Data(
                    data={'id': '1', 'name': 'customer'},
                )
            ],
        ),
        UpdateData(
            schema=SchemaReference(name='customers', namespace=namespace, version=Version.LATEST),
            data=Data(
                data={'id': '1', 'name': 'new_customer'},
            ),
        ),
    ])


async def delete_customer(database_connection: AsyncPostgresConnection, namespace: str = '') -> list[list[Data] | None]:
    return await database_connection.run_mutations([
        DeleteData(
            schema=SchemaReference(name='customers', namespace=namespace, version=Version.LATEST),
            query=Conditions(
                Condition(
                    left=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='age'), table_name='')
                    ),
                    lookup=FieldLookup.LT,
                    right=Value(27),
                ),
            ),
        ),
    ])
