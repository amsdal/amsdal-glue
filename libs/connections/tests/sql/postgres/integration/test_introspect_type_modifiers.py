"""Integration tests for M18: introspection must preserve type modifiers.

These require a live PostgreSQL (provided by the integration conftest, which spins up a
container when no server is reachable). The vector test additionally needs the ``pgvector``
extension and is skipped when it cannot be created.
"""

import pytest
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.types import ArrayType
from amsdal_glue_core.common.data_models.types import CustomType
from amsdal_glue_core.common.data_models.types import VectorType
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY


def _introspect_one(connection: PostgresConnection, table_name: str) -> Schema:
    schemas = connection.introspect_schema(
        QueryStatement(
            table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST),
            where=Conditions(
                Condition(
                    left=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='name'), table_name=TABLE_REGISTRY),
                    ),
                    lookup=FieldLookup.EQ,
                    right=Value(table_name),
                ),
            ),
        )
    )
    assert len(schemas) == 1
    return schemas[0]


def _prop_type(schema: Schema, name: str) -> object:
    return next(p.type for p in schema.properties if p.name == name)


def test_numeric_array_preserves_element_precision_and_scale(
    database_connection: PostgresConnection,
) -> None:
    database_connection.execute('CREATE TABLE prices (id INT, amounts NUMERIC(10, 2)[])')

    schema = _introspect_one(database_connection, 'prices')

    assert _prop_type(schema, 'amounts') == ArrayType(
        item_type=CustomType(name='NUMERIC', params={'precision': 10, 'scale': 2}),
    )


def test_vector_preserves_dimensions(database_connection: PostgresConnection) -> None:
    try:
        database_connection.execute('CREATE EXTENSION IF NOT EXISTS vector')
    except Exception as exc:  # noqa: BLE001 - pgvector may be unavailable in this environment
        pytest.skip(f'pgvector extension unavailable: {exc}')

    database_connection.execute('CREATE TABLE embeddings (id INT, embedding vector(3))')

    schema = _introspect_one(database_connection, 'embeddings')

    assert _prop_type(schema, 'embedding') == VectorType(dimensions=3)
