from pprint import pprint
from amsdal_glue import init_default_containers
from utils import (
    register_connections,
    create_schema_in_new_db,
    fetch_schemas,
    create_new_records,
    fetch_customers_and_their_shipping_status,
)


def main() -> None:
    init_default_containers()
    register_connections()

    # Create new schemas (tables)
    create_schema_in_new_db()

    # Fetch existing schemas (tables)
    all_schemas = fetch_schemas()

    print(f"All schemas from both databases (total: {len(all_schemas)}):")

    for schema in all_schemas:
        pprint(schema)

    # Create new records (rows)
    create_new_records()

    # Fetch existing records (rows)
    data = fetch_customers_and_their_shipping_status()

    print("Customers report:")

    for row in data:
        print(
            f"{row.data['first_name']} (ID: {row.data['customer_id']}) - Shipping status: {row.data['status']}"
        )


if __name__ == "__main__":
    main()
