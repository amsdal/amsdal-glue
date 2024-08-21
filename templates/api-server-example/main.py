# mypy: disable-error-code="type-abstract"
from collections.abc import Generator
from typing import Any

from amsdal_glue.connections.connection_pool import DefaultConnectionPool
from amsdal_glue.initialize import init_default_containers
from amsdal_glue_api_server.app import AmsdalGlueServerApp
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.containers import Container
from amsdal_glue_sql_parser.parsers.base import SqlParserBase
from amsdal_glue_sql_parser.parsers.sqloxide_parser import SqlOxideParser


def register_connections() -> Generator[Any, Any, Any]:
    init_default_containers()
    Container.services.register(SqlParserBase, SqlOxideParser)

    db1 = DefaultConnectionPool(
        SqliteConnection,
        db_path="customers_and_products.sqlite3",
        check_same_thread=False,
    )
    db2 = DefaultConnectionPool(
        SqliteConnection,
        db_path="cart.sqlite3",
        check_same_thread=False,
    )
    db3 = DefaultConnectionPool(
        SqliteConnection,
        db_path="logs.sqlite3",
        check_same_thread=False,
    )

    connection_mng = Container.managers.get(ConnectionManager)
    connection_mng.register_connection_pool(db1)
    connection_mng.register_connection_pool(db2, schema_name="orders")
    connection_mng.register_connection_pool(db2, schema_name="cart")
    connection_mng.register_connection_pool(db3, schema_name="logs")


register_connections()

AmsdalGlueServerApp().run()
