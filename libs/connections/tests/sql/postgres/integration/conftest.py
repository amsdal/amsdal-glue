import contextlib
import os
import uuid
from collections.abc import Generator
from contextlib import suppress
from dataclasses import dataclass
from time import sleep
from typing import Any

import pytest

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection


@dataclass
class ConnectionInfo:
    host: str
    port: str
    user: str
    password: str
    connection: Any


def get_postgres_credentials() -> tuple[str, str, str, str]:
    db_host = os.getenv('POSTGRES_HOST', 'localhost')
    db_port = os.getenv('POSTGRES_PORT', '5432')
    db_user = os.getenv('POSTGRES_USER', 'postgres')
    db_password = os.getenv('POSTGRES_PASSWORD', 'example')

    return db_host, db_port, db_user, db_password


@contextlib.contextmanager
def get_postgres_connection_info() -> Generator[ConnectionInfo, None, None]:
    import psycopg

    (
        db_host,
        db_port,
        db_user,
        db_password,
    ) = get_postgres_credentials()

    conn = psycopg.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        autocommit=True,
    )

    yield ConnectionInfo(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        connection=conn,
    )

    conn.close()


def create_postgres_database(database: str) -> tuple[str, str, str, str]:
    import psycopg

    with get_postgres_connection_info() as conn_info:
        cur = conn_info.connection.cursor()

        with suppress(psycopg.errors.DuplicateDatabase):
            cur.execute(f'CREATE DATABASE "{database}"')

        cur.close()

    return (
        conn_info.host,
        conn_info.port,
        conn_info.user,
        conn_info.password,
    )


def delete_postgres_database(database: str) -> None:
    import psycopg

    with get_postgres_connection_info() as conn_info:
        cur = conn_info.connection.cursor()

        with suppress(psycopg.errors.InvalidCatalogName):
            cur.execute(f'DROP DATABASE "{database}"')

        cur.close()


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
        delete_postgres_database(db_name)


@pytest.fixture(scope='session', autouse=True)
def _postgres_server_run() -> Generator[None, None, None]:
    import psycopg

    container = None

    try:
        with get_postgres_connection_info():
            ...
    except psycopg.OperationalError:
        import docker

        client = docker.from_env()
        (
            db_host,
            db_port,
            db_user,
            db_password,
        ) = get_postgres_credentials()
        container = client.containers.run(
            image='postgres:latest',
            auto_remove=True,
            environment={'POSTGRES_USER': db_user, 'POSTGRES_PASSWORD': db_password},
            name='test_postgres',
            ports={'5432/tcp': ('127.0.0.1', db_port)},
            detach=True,
            remove=True,
        )
        is_connected = False

        while retry_count := 5:
            try:
                with get_postgres_connection_info():
                    is_connected = True
                    break
            except psycopg.OperationalError:
                sleep(5)
                retry_count -= 1

        if not is_connected:
            msg = 'Failed to start postgres server'
            raise RuntimeError(msg)  # noqa: B904

    yield

    if container:
        container.stop()
