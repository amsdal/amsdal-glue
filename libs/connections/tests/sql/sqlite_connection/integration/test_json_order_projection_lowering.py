"""SQLite JSON-extraction lowering in ORDER BY / SELECT projection.

On SQLite the canonical Postgres `col->'k'` form returns JSON *text*, so a nested JSON field left
un-lowered in ORDER BY sorts lexically (`10 < 2 < 36`) and a projected subkey comes back as quoted
JSON text. `lower_query` must lower those positions to the native `->>` form -- the same treatment
WHERE already gets: `jsonb_extract` semantics give numeric ordering and native values.
"""

from __future__ import annotations

from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection

from tests.sql.json_output_type_cases import register_and_seed

TABLE = 'JsonOrderProj'
ROWS = [
    {'id': 2, 'payload': {'age': 2, 'name': 'hello'}},
    {'id': 10, 'payload': {'age': 10, 'name': 'world'}},
    {'id': 36, 'payload': {'age': 36, 'name': 'zeta'}},
    {'id': 100, 'payload': {'age': 100, 'name': 'alpha'}},
]


def _age_ref() -> FieldReferenceExpression:
    return FieldReferenceExpression(
        field_reference=FieldReference(field=Field(name='payload', child=Field(name='age')), table_name=TABLE),
    )


def test_order_by_json_subkey_is_numeric(database_connection: SqliteConnection) -> None:
    register_and_seed(database_connection, TABLE, ROWS)

    query = QueryStatement(
        table=SchemaReference(name=TABLE, version=Version.LATEST),
        order_by=[OrderByQuery(expression=_age_ref(), direction=OrderDirection.ASC)],
    )

    result = database_connection.query(query)
    ordered_ages = [row.data['payload']['age'] for row in result]

    # Numeric order, NOT the lexical [10, 100, 2, 36] the un-lowered `->` form produces.
    assert ordered_ages == [2, 10, 36, 100]


def test_projected_json_subkey_returns_native_value(database_connection: SqliteConnection) -> None:
    register_and_seed(database_connection, TABLE, ROWS)

    query = QueryStatement(
        table=SchemaReference(name=TABLE, version=Version.LATEST),
        only=[FieldReference(field=Field(name='payload', child=Field(name='name')), table_name=TABLE)],
        order_by=[OrderByQuery(expression=_age_ref(), direction=OrderDirection.ASC)],
    )

    result = database_connection.query(query)
    projected = [next(iter(row.data.values())) for row in result]

    # Native string values, NOT the quoted JSON text (`'"hello"'`) the un-lowered `->` form returns.
    assert projected == ['hello', 'world', 'zeta', 'alpha']
