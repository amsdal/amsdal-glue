"""Integration test for pgvector param binding (code-review finding #11).

``postgres_connection/base.py`` registers a process-global ``list -> jsonb`` dumper
(``psycopg.adapters.register_dumper(list, JsonbBinaryDumper)``). The open question was whether
that dumper also captures a pgvector parameter and binds it as ``jsonb`` instead of a ``vector``
literal — which would either fail the INSERT (no ``jsonb -> vector`` cast) or store garbage.

These tests drive a real ``Vector`` value through the normal glue mutation path into a
``vector(N)`` column and read it back, asserting it round-trips as a proper vector.

The ``database_connection`` fixture (conftest.py) provisions a dedicated, randomly-named database
per test and drops it on teardown, so no shared state is disturbed. pgvector is available because the
server runs the ``pgvector/pgvector`` image; the extension is created per test database below.
"""

from collections.abc import Generator

import pytest
from amsdal_glue_core.common.data_models.data import DataInput
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.vector import Vector
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.mutations.data import InsertData

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection


@pytest.fixture(scope='function')
def vector_connection(database_connection: PostgresConnection) -> Generator[PostgresConnection, None, None]:
    database_connection.execute('CREATE EXTENSION IF NOT EXISTS vector')
    database_connection.execute('CREATE TABLE items (id INT PRIMARY KEY, embedding vector(3))')
    yield database_connection


def test_vector_binds_as_vector_not_jsonb(vector_connection: PostgresConnection) -> None:
    """A ``Vector`` value inserted through glue must bind as a vector literal, not jsonb.

    If the global ``list -> jsonb`` dumper captured the param, this INSERT would raise (there is no
    implicit ``jsonb -> vector`` cast). The ``Vector`` extractor emits a ``'[1,2,3]'`` string param,
    which Postgres casts straight to ``vector`` — so the dumper never sees a ``list`` here.
    """
    vector_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name='items', version=Version.LATEST),
            data=[DataInput(data={'id': '1', 'embedding': Vector(values=[1.0, 2.0, 3.0])})],
        ),
    ])

    # The column really is a vector (not jsonb), and the stored value is the vector we inserted.
    col_type = vector_connection.execute(
        "SELECT udt_name FROM information_schema.columns WHERE table_name = 'items' AND column_name = 'embedding'"
    ).fetchall()
    assert col_type == [('vector',)]

    stored = vector_connection.execute('SELECT embedding::text FROM items WHERE id = 1').fetchall()
    assert stored == [('[1,2,3]',)]


def test_vector_distance_query_uses_stored_vector(vector_connection: PostgresConnection) -> None:
    """The stored value behaves as a real vector: a distance operator resolves against it.

    ``jsonb`` has no ``<->`` operator, so this only works if the value was bound as a genuine vector.
    """
    vector_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name='items', version=Version.LATEST),
            data=[DataInput(data={'id': '1', 'embedding': Vector(values=[1.0, 2.0, 3.0])})],
        ),
    ])

    distance = vector_connection.execute("SELECT embedding <-> '[1,2,3]'::vector FROM items WHERE id = 1").fetchall()
    assert distance == [(0.0,)]
