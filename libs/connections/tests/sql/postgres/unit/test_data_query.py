from typing import Any
from unittest import mock

from tests.sql.postgres.testcases.data_query import query_big_orders
from tests.sql.postgres.testcases.data_query import query_customers
from tests.sql.postgres.testcases.data_query import query_customers_age
from tests.sql.postgres.testcases.data_query import query_customers_expenses
from tests.sql.postgres.testcases.data_query import query_expenses_by_customer
from tests.sql.postgres.testcases.data_query import query_expenses_by_customer_with_name
from tests.sql.postgres.testcases.data_query import query_orders_for_customer
from tests.sql.postgres.testcases.data_query import query_orders_with_customers
from tests.sql.postgres.unit.conftest import MockPostgresConnection


class CursorMock(mock.Mock):
    def __init__(self, description: list[tuple[str, ...]], results: list[tuple[Any, ...]], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.execute = mock.Mock()
        self.description = description
        self._results = results

    def fetchall(self) -> list[tuple[Any, ...]]:
        return self._results

    def close(self) -> None:
        pass


def _query_customers_mock() -> CursorMock:
    return CursorMock(
        description=[('id',), ('name',), ('age',)],
        results=[
            (1, 'Alice', 25),
            (2, 'Bob', 25),
            (3, 'Charlie', 35),
        ],
    )


def test_simple_query(database_connection: MockPostgresConnection) -> None:
    database_connection.set_cursor_mock(_query_customers_mock())

    result_data = query_customers(database_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'name': 'Alice', 'age': 25},
        {'id': 2, 'name': 'Bob', 'age': 25},
        {'id': 3, 'name': 'Charlie', 'age': 35},
    ]

    database_connection.connection.execute.assert_called_once_with(
        'SELECT * FROM "customers" AS "c" ORDER BY "c"."id" ASC',
        (),
    )


def test_simple_query_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    database_connection.set_cursor_mock(_query_customers_mock())

    def _run_query() -> None:
        query_customers(database_connection)

    benchmark(_run_query)


def _join_query_mock() -> CursorMock:
    return CursorMock(
        description=[('id',), ('amount',), ('customer_id',), ('name',), ('age',)],
        results=[
            (1, 100, 1, 'Alice', 25),
            (2, 200, 1, 'Alice', 25),
            (3, 400, 2, 'Bob', 25),
        ],
    )


def test_join_query(database_connection: MockPostgresConnection) -> None:
    database_connection.set_cursor_mock(_join_query_mock())

    result_data = query_orders_with_customers(database_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'amount': 100, 'customer_id': 1, 'name': 'Alice', 'age': 25},
        {'id': 2, 'amount': 200, 'customer_id': 1, 'name': 'Alice', 'age': 25},
        {'id': 3, 'amount': 400, 'customer_id': 2, 'name': 'Bob', 'age': 25},
    ]

    database_connection.connection.execute.assert_called_once_with(
        'SELECT "o"."id", "o"."amount", "o"."customer_id", "c"."name", "c"."age" '
        'FROM "orders" AS "o" '
        'INNER JOIN "customers" AS "c" ON "o"."customer_id" = "c"."id" '
        'ORDER BY "o"."id" ASC',
        (),
    )


def test_join_query_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    database_connection.set_cursor_mock(_join_query_mock())

    def _run_query() -> None:
        query_orders_with_customers(database_connection)

    benchmark(_run_query)


def _query_distinct_mock() -> CursorMock:
    return CursorMock(
        description=[('age',)],
        results=[
            (25,),
            (35,),
        ],
    )


def test_query_distinct(database_connection: MockPostgresConnection) -> None:
    database_connection.set_cursor_mock(_query_distinct_mock())

    result_data = query_customers_age(database_connection, distinct=True)

    assert [d.data for d in result_data] == [
        {'age': 25},
        {'age': 35},
    ]

    database_connection.connection.execute.assert_called_once_with(
        'SELECT DISTINCT "c"."age" FROM "customers" AS "c" ORDER BY "c"."age" ASC',
        (),
    )


def test_query_distinct_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    database_connection.set_cursor_mock(_query_distinct_mock())

    def _run_query() -> None:
        query_customers_age(database_connection, distinct=True)

    benchmark(_run_query)


def _filter_conditions_mock() -> CursorMock:
    return CursorMock(
        description=[('id',), ('amount',), ('customer_id',)],
        results=[
            (2, 200, 1),
            (3, 400, 2),
        ],
    )


def test_filter_conditions(database_connection: MockPostgresConnection) -> None:
    database_connection.set_cursor_mock(_filter_conditions_mock())

    result_data = query_big_orders(database_connection)

    assert [d.data for d in result_data] == [
        {'id': 2, 'amount': 200, 'customer_id': 1},
        {'id': 3, 'amount': 400, 'customer_id': 2},
    ]

    database_connection.connection.execute.assert_called_once_with(
        (
            'SELECT "o"."id", "o"."amount", "o"."customer_id" '
            'FROM "orders" AS "o" WHERE "o"."amount" > %s ORDER BY "o"."id" ASC'
        ),
        (100,),
    )


def test_filter_conditions_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    database_connection.set_cursor_mock(_filter_conditions_mock())

    def _run_query() -> None:
        query_big_orders(database_connection)

    benchmark(_run_query)


def _filter_conditions_join_mock() -> CursorMock:
    return CursorMock(
        description=[('id',), ('amount',), ('customer_id',), ('age',)],
        results=[
            (1, 100, 1, 25),
            (2, 200, 1, 25),
        ],
    )


def test_filter_conditions_join(database_connection: MockPostgresConnection) -> None:
    database_connection.set_cursor_mock(_filter_conditions_join_mock())

    result_data = query_orders_for_customer(database_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'amount': 100, 'customer_id': 1, 'age': 25},
        {'id': 2, 'amount': 200, 'customer_id': 1, 'age': 25},
    ]

    database_connection.connection.execute.assert_called_once_with(
        'SELECT "o"."id", "o"."amount", "o"."customer_id", "c"."age" '
        'FROM "orders" AS "o" '
        'INNER JOIN "customers" AS "c" ON "o"."customer_id" = "c"."id" '
        'WHERE "c"."name" = %s ORDER BY "o"."id" ASC',
        ('Alice',),
    )


def test_filter_conditions_join_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    database_connection.set_cursor_mock(_filter_conditions_join_mock())

    def _run_query() -> None:
        query_orders_for_customer(database_connection)

    benchmark(_run_query)


def _annotation_mock() -> CursorMock:
    return CursorMock(
        description=[('id',), ('total_amount',)],
        results=[
            (1, 300),
            (2, 400),
            (3, None),
        ],
    )


def test_annotation(database_connection: MockPostgresConnection) -> None:
    database_connection.set_cursor_mock(_annotation_mock())

    result_data = query_customers_expenses(database_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'total_amount': 300},
        {'id': 2, 'total_amount': 400},
        {'id': 3, 'total_amount': None},
    ]

    database_connection.connection.execute.assert_called_once_with(
        'SELECT "c"."id", (SELECT SUM("o"."amount") AS "total_amount" FROM "orders" AS "o" '
        'WHERE "o"."customer_id" = "c"."id") AS "total_amount" '
        'FROM "customers" AS "c" '
        'ORDER BY "c"."id" ASC',
        (),
    )


def test_annotation_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    database_connection.set_cursor_mock(_annotation_mock())

    def _run_query() -> None:
        query_customers_expenses(database_connection)

    benchmark(_run_query)


def _aggregation_mock() -> CursorMock:
    return CursorMock(
        description=[('customer_id',), ('total_amount',)],
        results=[
            (1, 300),
            (2, 400),
        ],
    )


def test_aggregation(database_connection: MockPostgresConnection) -> None:
    database_connection.set_cursor_mock(_aggregation_mock())

    result_data = query_expenses_by_customer(database_connection)

    assert [d.data for d in result_data] == [
        {'customer_id': 1, 'total_amount': 300},
        {'customer_id': 2, 'total_amount': 400},
    ]

    database_connection.connection.execute.assert_called_once_with(
        'SELECT "o"."customer_id", SUM("o"."amount") AS "total_amount" '
        'FROM "orders" AS "o" '
        'GROUP BY "o"."customer_id" '
        'ORDER BY "o"."customer_id" ASC',
        (),
    )


def test_aggregation_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    database_connection.set_cursor_mock(_aggregation_mock())

    def _run_query() -> None:
        query_expenses_by_customer(database_connection)

    benchmark(_run_query)


def _aggregation_join_mock() -> CursorMock:
    return CursorMock(
        description=[('id',), ('name',), ('sum_amount',)],
        results=[
            (1, 'Alice', 300),
            (2, 'Bob', 400),
        ],
    )


def test_aggregation_join(database_connection: MockPostgresConnection) -> None:
    database_connection.set_cursor_mock(_aggregation_join_mock())

    result_data = query_expenses_by_customer_with_name(database_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'name': 'Alice', 'sum_amount': 300},
        {'id': 2, 'name': 'Bob', 'sum_amount': 400},
    ]

    database_connection.connection.execute.assert_called_once_with(
        'SELECT "customers"."id", "customers"."name", SUM("orders"."amount") AS "sum_amount" '
        'FROM "orders" INNER JOIN "customers" ON "customers"."id" = "orders"."customer_id" '
        'GROUP BY "customers"."id", "customers"."name" '
        'ORDER BY "customers"."id" ASC',
        (),
    )


def test_aggregation_join_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    database_connection.set_cursor_mock(_aggregation_join_mock())

    def _run_query() -> None:
        query_expenses_by_customer_with_name(database_connection)

    benchmark(_run_query)
