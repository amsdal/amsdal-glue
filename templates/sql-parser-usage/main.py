from amsdal_glue.initialize import init_default_containers
from utils import (
    register_connections,
    register_parser,
    create_schemas,
    create_new_records,
)

from amsdal_glue_sql_parser.parsers.base import SqlParserBase

from amsdal_glue_core.common.services.queries import DataQueryService

from amsdal_glue_core.containers import Container


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
