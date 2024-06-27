import os
import uuid
from collections.abc import Generator
from contextlib import suppress

import pytest
from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from amsdal_glue_core.common.helpers.singleton import Singleton


def create_postgres_database(database: str) -> tuple[str, str, str, str]:
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    db_host = os.getenv('POSTGRES_HOST', 'localhost')
    db_port = os.getenv('POSTGRES_PORT', '5432')
    db_user = os.getenv('POSTGRES_USER', 'postgres')
    db_password = os.getenv('POSTGRES_PASSWORD', 'example')

    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    with suppress(psycopg2.errors.DuplicateDatabase):
        cur.execute(f'CREATE DATABASE "{database}"')

    cur.close()
    conn.close()

    return (
        db_host,
        db_port,
        db_user,
        db_password,
    )


def delete_postgres_database(database: str) -> None:
    import psycopg2

    db_host = os.getenv('POSTGRES_HOST', 'localhost')
    db_port = os.getenv('POSTGRES_PORT', '5432')
    db_user = os.getenv('POSTGRES_USER', 'postgres')
    db_password = os.getenv('POSTGRES_PASSWORD', 'example')

    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
    )
    conn.set_isolation_level(0)
    cur = conn.cursor()

    with suppress(psycopg2.errors.InvalidCatalogName):
        cur.execute(f'DROP DATABASE "{database}"')

    cur.close()
    conn.close()


@pytest.fixture(scope='function')
def database_connection() -> Generator[PostgresConnection, None, None]:
    db_name = uuid.uuid4().hex

    (
        db_host,
        db_port,
        db_user,
        db_password,
    ) = create_postgres_database(db_name)

    connection = PostgresConnection()
    connection.connect(dsn=f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

    try:
        yield connection
    finally:
        connection.disconnect()
        delete_postgres_database(connection)
        Singleton.invalidate_all_instances()
