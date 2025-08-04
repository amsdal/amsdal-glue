from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.elasticsearch_connection.sync_connection import ElasticsearchConnection


def test_simple_table_info(database_connection: ElasticsearchConnection, test_prefix: str) -> None:
    # Create customers index
    customers_schema = Schema(
        name='customers',
        version=Version.LATEST,
        properties=[
            PropertySchema(name='id', type=int, required=True, description=None, default=None),
            PropertySchema(name='name', type=str, required=False, description=None, default=None),
            PropertySchema(name='age', type=int, required=False, description=None, default=None),
        ],
        constraints=[PrimaryKeyConstraint(name='customers_pkey', fields=['id'])],
        indexes=[],
    )

    customers_command = SchemaCommand(mutations=[RegisterSchema(schema=customers_schema)])
    database_connection.run_schema_command(customers_command)

    # Create orders index
    orders_schema = Schema(
        name='orders',
        version=Version.LATEST,
        properties=[
            PropertySchema(name='id', type=int, required=True, description=None, default=None),
            PropertySchema(name='customer_id', type=int, required=False, description=None, default=None),
            PropertySchema(name='amount', type=int, required=False, description=None, default=None),
            PropertySchema(
                name='date', type=str, required=False, description=None, default=None
            ),  # ES doesn't have date type like SQL
        ],
        constraints=[PrimaryKeyConstraint(name='orders_pkey', fields=['id'])],
        indexes=[],
    )

    orders_command = SchemaCommand(mutations=[RegisterSchema(schema=orders_schema)])
    database_connection.run_schema_command(orders_command)

    # Test get_table_info for orders index
    properties, constraints, indexes = database_connection.get_table_info('orders')

    # Check properties (Elasticsearch doesn't preserve order, so we need to sort)
    # Note: Elasticsearch doesn't have native "required" concept, so all fields are required=False when retrieved
    expected_properties = [
        PropertySchema(name='id', type=int, required=False, description=None, default=None),
        PropertySchema(name='customer_id', type=int, required=False, description=None, default=None),
        PropertySchema(name='amount', type=int, required=False, description=None, default=None),
        PropertySchema(name='date', type=str, required=False, description=None, default=None),
    ]

    # Sort both lists by property name for comparison
    properties_sorted = sorted(properties, key=lambda p: p.name)
    expected_properties_sorted = sorted(expected_properties, key=lambda p: p.name)

    assert properties_sorted == expected_properties_sorted

    # Check constraints (Elasticsearch stores constraints in metadata)
    expected_constraints = [
        PrimaryKeyConstraint(name='orders_pkey', fields=['id']),
    ]
    assert constraints == expected_constraints

    # Check indexes (empty for this test)
    assert indexes == []

    # Test query_schema() method
    schemas = database_connection.query_schema()

    # Elasticsearch may return schemas in any order, and properties may also be in any order
    # So we need to sort for comparison
    schemas_by_name = {schema.name.replace(test_prefix, ''): schema for schema in schemas}

    # Expected customers schema
    expected_customers = Schema(
        name=f'{test_prefix}customers',  # Elasticsearch returns full index name with prefix
        version=Version.LATEST,
        extends=None,
        properties=[
            PropertySchema(name='age', type=int, required=False, description=None, default=None),
            PropertySchema(
                name='id', type=int, required=False, description=None, default=None
            ),  # ES doesn't have required concept
            PropertySchema(name='name', type=str, required=False, description=None, default=None),
        ],
        constraints=[PrimaryKeyConstraint(name='customers_pkey', fields=['id'])],
        indexes=[],
    )

    # Expected orders schema
    expected_orders = Schema(
        name=f'{test_prefix}orders',  # Elasticsearch returns full index name with prefix
        version=Version.LATEST,
        extends=None,
        properties=[
            PropertySchema(name='amount', type=int, required=False, description=None, default=None),
            PropertySchema(name='customer_id', type=int, required=False, description=None, default=None),
            PropertySchema(name='date', type=str, required=False, description=None, default=None),
            PropertySchema(
                name='id', type=int, required=False, description=None, default=None
            ),  # ES doesn't have required concept
        ],
        constraints=[PrimaryKeyConstraint(name='orders_pkey', fields=['id'])],
        indexes=[],
    )

    # Check that both schemas exist
    assert 'customers' in schemas_by_name
    assert 'orders' in schemas_by_name

    # Compare customers schema (sorting properties for comparison)
    customers_schema = schemas_by_name['customers']
    customers_properties_sorted = sorted(customers_schema.properties, key=lambda p: p.name)
    expected_customers_properties_sorted = sorted(expected_customers.properties, key=lambda p: p.name)

    assert customers_schema.name == expected_customers.name
    assert customers_properties_sorted == expected_customers_properties_sorted
    assert customers_schema.constraints == expected_customers.constraints
    assert customers_schema.indexes == expected_customers.indexes

    # Compare orders schema (sorting properties for comparison)
    orders_schema = schemas_by_name['orders']
    orders_properties_sorted = sorted(orders_schema.properties, key=lambda p: p.name)
    expected_orders_properties_sorted = sorted(expected_orders.properties, key=lambda p: p.name)

    assert orders_schema.name == expected_orders.name
    assert orders_properties_sorted == expected_orders_properties_sorted
    assert orders_schema.constraints == expected_orders.constraints
    assert orders_schema.indexes == expected_orders.indexes
