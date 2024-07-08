from pprint import pprint
from amsdal_glue.initialize import init_default_containers
from utils import *


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
            f'{row.data["first_name"]} (ID: {row.data["customer_id"]}) - Shipping status: {row.data["status"]}'
        )


if __name__ == "__main__":
    main()
