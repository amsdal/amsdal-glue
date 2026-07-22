"""Postgres JSON ORDER BY / projection lowering.

Postgres renders the canonical AST directly (no SQLite lowering), so it already orders a JSON subkey
numerically and projects native values. This pins that the SQLite lowering fix does NOT disturb the
Postgres path -- both dialects must agree.
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

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection

from tests.sql.json_output_type_cases import register_and_seed

TABLE = 'JsonOrderProjPg'
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


def test_order_by_json_subkey_is_numeric(database_connection: PostgresConnection) -> None:
    register_and_seed(database_connection, TABLE, ROWS)

    query = QueryStatement(
        table=SchemaReference(name=TABLE, version=Version.LATEST),
        order_by=[OrderByQuery(expression=_age_ref(), direction=OrderDirection.ASC)],
    )

    result = database_connection.query(query)
    ordered_ages = [row.data['payload']['age'] for row in result]

    assert ordered_ages == [2, 10, 36, 100]


def test_projected_json_subkey_returns_native_value(database_connection: PostgresConnection) -> None:
    register_and_seed(database_connection, TABLE, ROWS)

    query = QueryStatement(
        table=SchemaReference(name=TABLE, version=Version.LATEST),
        only=[FieldReference(field=Field(name='payload', child=Field(name='name')), table_name=TABLE)],
        order_by=[OrderByQuery(expression=_age_ref(), direction=OrderDirection.ASC)],
    )

    result = database_connection.query(query)
    projected = [next(iter(row.data.values())) for row in result]

    assert projected == ['hello', 'world', 'zeta', 'alpha']
