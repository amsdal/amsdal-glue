import datetime

from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection


def test_simple_table_info(database_connection: PostgresConnection) -> None:
    database_connection.execute(
        'CREATE TABLE customers (id SERIAL PRIMARY KEY, name VARCHAR(255), age INT)',
    )

    database_connection.execute(
        'CREATE TABLE orders ('
        'id SERIAL PRIMARY KEY, customer_id INT, amount INT, date DATE, '
        'FOREIGN KEY (customer_id) REFERENCES customers (id))'
    )

    database_connection.execute('CREATE INDEX orders_customer_id_idx ON orders (customer_id)')

    assert (
        [
            PropertySchema(
                name='id', type=int, required=True, description=None, default="nextval('orders_id_seq'::regclass)"
            ),
            PropertySchema(name='customer_id', type=int, required=False, description=None, default=None),
            PropertySchema(name='amount', type=int, required=False, description=None, default=None),
            PropertySchema(name='date', type=datetime.date, required=False, description=None, default=None),
        ],
        [
            PrimaryKeyConstraint(
                name='orders_pkey',
                fields=[
                    'id',
                ],
            ),
            ForeignKeyConstraint(
                name='orders_customer_id_fkey',
                fields=['customer_id'],
                reference_schema=SchemaReference(name='customers', version=Version.LATEST, alias=None),
                reference_fields=['id'],
            ),
        ],
        [],
    ) == database_connection.get_table_info('orders')

    assert [
        Schema(
            name='customers',
            version=Version.LATEST,
            extends=None,
            properties=[
                PropertySchema(
                    name='id',
                    type=int,
                    required=True,
                    description=None,
                    default="nextval('customers_id_seq'::regclass)",
                ),
                PropertySchema(name='age', type=int, required=False, description=None, default=None),
                PropertySchema(name='name', type=str, required=False, description=None, default=None),
            ],
            constraints=[PrimaryKeyConstraint(name='customers_pkey', fields=['id'])],
            indexes=[],
        ),
        Schema(
            name='orders',
            version=Version.LATEST,
            extends=None,
            properties=[
                PropertySchema(
                    name='id', type=int, required=True, description=None, default="nextval('orders_id_seq'::regclass)"
                ),
                PropertySchema(name='customer_id', type=int, required=False, description=None, default=None),
                PropertySchema(name='amount', type=int, required=False, description=None, default=None),
                PropertySchema(name='date', type=datetime.date, required=False, description=None, default=None),
            ],
            constraints=[
                PrimaryKeyConstraint(name='orders_pkey', fields=['id']),
                ForeignKeyConstraint(
                    name='orders_customer_id_fkey',
                    fields=['customer_id'],
                    reference_schema=SchemaReference(name='customers', version=Version.LATEST, alias=None),
                    reference_fields=['id'],
                ),
            ],
            indexes=[],
        ),
    ] == database_connection.query_schema()
