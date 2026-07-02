from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY


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

    assert database_connection.introspect_schema(
        QueryStatement(
            table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST),
            where=Conditions(
                Condition(
                    left=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='name'), table_name=TABLE_REGISTRY)
                    ),
                    lookup=FieldLookup.EQ,
                    right=Value('orders'),
                ),
            ),
        )
    ) == [
        Schema(
            name='orders',
            version=Version.LATEST,
            namespace='public',
            properties=[
                PropertySchema(name='id', type=ScalarType.SERIAL, required=True, description=None, default=None),
                PropertySchema(
                    name='customer_id', type=ScalarType.INTEGER, required=False, description=None, default=None
                ),
                PropertySchema(name='amount', type=ScalarType.INTEGER, required=False, description=None, default=None),
                PropertySchema(name='date', type=ScalarType.DATE, required=False, description=None, default=None),
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
            indexes=[
                IndexSchema(
                    name='orders_customer_id_idx',
                    fields=[IndexField(name='customer_id')],
                ),
            ],
        ),
    ]

    assert database_connection.introspect_schema(
        QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
    ) == [
        Schema(
            name='customers',
            version=Version.LATEST,
            namespace='public',
            properties=[
                PropertySchema(name='id', type=ScalarType.SERIAL, required=True, description=None, default=None),
                PropertySchema(name='name', type=ScalarType.TEXT, required=False, description=None, default=None),
                PropertySchema(name='age', type=ScalarType.INTEGER, required=False, description=None, default=None),
            ],
            constraints=[PrimaryKeyConstraint(name='customers_pkey', fields=['id'])],
            indexes=None,
        ),
        Schema(
            name='orders',
            version=Version.LATEST,
            namespace='public',
            properties=[
                PropertySchema(name='id', type=ScalarType.SERIAL, required=True, description=None, default=None),
                PropertySchema(
                    name='customer_id', type=ScalarType.INTEGER, required=False, description=None, default=None
                ),
                PropertySchema(name='amount', type=ScalarType.INTEGER, required=False, description=None, default=None),
                PropertySchema(name='date', type=ScalarType.DATE, required=False, description=None, default=None),
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
            indexes=[
                IndexSchema(
                    name='orders_customer_id_idx',
                    fields=[IndexField(name='customer_id')],
                ),
            ],
        ),
    ]
