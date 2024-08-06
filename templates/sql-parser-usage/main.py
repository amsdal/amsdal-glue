from amsdal_glue_sql_parser.parsers.base import SqlParserBase

from amsdal_glue import Container
from amsdal_glue.initialize import init_default_containers
from amsdal_glue.interfaces import DataQueryService
from amsdal_glue.interfaces import SchemaQueryService
from utils import create_new_records
from utils import create_schemas
from utils import register_connections
from utils import register_parser


def main() -> None:
    init_default_containers()
    register_connections()
    register_parser()

    # Create new schemas (tables)
    create_schemas()

    # # Create new records (rows)
    create_new_records()

    # Fetch existing records (rows)
    service = Container.services.get(DataQueryService)
    parser = Container.services.get(SqlParserBase)
    schema_query_service = Container.services.get(SchemaQueryService)

    schema_result = schema_query_service.execute(
        query_op=parser.parse_sql("SELECT * FROM amsdal_schema_registry")[0]
    )
    assert schema_result.success is True, schema_result
    print("Schema Registry:")
    for schema in schema_result.schemas:
        print(f" Table: {schema.name}")
        for property in schema.properties:
            print(f"  - {property.name} ({property.type})")
        print()

    print()
    print()

    data_result = service.execute(
        query_op=parser.parse_sql(
            "SELECT id, product, price, customers.first_name, customers.last_name "
            "FROM orders JOIN customers ON customers.id = orders.customer_id "
            "ORDER BY orders.id ASC, customers.id ASC"
        )[0]
    )
    assert data_result.success is True, data_result

    print("Orders:")
    for row in data_result.data:
        print(
            f'{row.data["product"]} ${row.data["price"]} (ID: {row.data["id"]}) - Buyer: {row.data["first_name"]} {row.data["last_name"]}'
        )

    print()

    data_result = service.execute(
        query_op=parser.parse_sql(
            "SELECT customers.first_name, customers.last_name, SUM(price) as sum_price "
            "FROM orders JOIN customers ON customers.id = orders.customer_id "
            "GROUP BY customers.first_name, customers.last_name "
            "ORDER BY customers.first_name ASC "
        )[0]
    )

    print("Total spent by each customer:")
    for row in data_result.data:
        print(
            f'{row.data["first_name"]} {row.data["last_name"]}: ${row.data["sum_price"]}'
        )


if __name__ == "__main__":
    main()
