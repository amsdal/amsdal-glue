from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.metadata import Metadata
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.data import DeleteData
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateData


def simple_customer_insert(database_connection: PostgresConnection) -> list[list[Data] | None]:
    return database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name='customers', version=Version.LATEST),
            data=[
                Data(
                    data={'id': '1', 'name': 'customer'},
                    metadata=Metadata(
                        object_id='1',
                        object_version='1',
                        created_at='2021-01-01T00:00:00Z',
                        updated_at='2021-01-01T00:00:00Z',
                    ),
                )
            ],
        ),
    ])


def insert_customers_and_orders(database_connection: PostgresConnection) -> list[list[Data] | None]:
    return database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name='customers', version=Version.LATEST),
            data=[
                Data(
                    data={'id': '1', 'name': 'customer'},
                    metadata=Metadata(
                        object_id='1',
                        object_version='1',
                        created_at='2021-01-01T00:00:00Z',
                        updated_at='2021-01-01T00:00:00Z',
                    ),
                )
            ],
        ),
        InsertData(
            schema=SchemaReference(name='customers', version=Version.LATEST),
            data=[
                Data(
                    data={'id': '2', 'name': 'customer', 'age': 25},
                    metadata=Metadata(
                        object_id='2',
                        object_version='2',
                        created_at='2021-01-01T00:00:00Z',
                        updated_at='2021-01-01T00:00:00Z',
                    ),
                )
            ],
        ),
        InsertData(
            schema=SchemaReference(name='orders', version=Version.LATEST),
            data=[
                Data(
                    data={'id': '1', 'customer_id': '1', 'amount': 100},
                    metadata=Metadata(
                        object_id='1',
                        object_version='1',
                        created_at='2021-01-01T00:00:00Z',
                        updated_at='2021-01-01T00:00:00Z',
                    ),
                )
            ],
        ),
    ])


def update_two_customers(database_connection: PostgresConnection) -> list[list[Data] | None]:
    return database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name='customers', version=Version.LATEST),
            data=[
                Data(
                    data={'id': '1', 'name': 'customer'},
                    metadata=Metadata(
                        object_id='1',
                        object_version='1',
                        created_at='2021-01-01T00:00:00Z',
                        updated_at='2021-01-01T00:00:00Z',
                    ),
                )
            ],
        ),
        UpdateData(
            schema=SchemaReference(name='customers', version=Version.LATEST),
            data=Data(
                data={'id': '1', 'name': 'new_customer'},
                metadata=Metadata(
                    object_id='1',
                    object_version='2',
                    created_at='2021-01-01T00:00:00Z',
                    updated_at='2021-01-01T00:00:00Z',
                ),
            ),
        ),
    ])


def delete_customer(database_connection: PostgresConnection) -> list[list[Data] | None]:
    return database_connection.run_mutations([
        DeleteData(
            schema=SchemaReference(name='customers', version=Version.LATEST),
            query=Conditions(
                Condition(
                    field=FieldReference(field=Field(name='age'), table_name=''),
                    lookup=FieldLookup.LT,
                    value=Value(27),
                ),
            ),
        ),
    ])
