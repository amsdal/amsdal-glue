# mypy: disable-error-code="type-abstract"
import datetime
import tempfile
from collections.abc import Generator
from typing import Any

import pytest
from amsdal_glue.connections.connection_pool import DefaultConnectionPool
from amsdal_glue.initialize import init_default_containers
from amsdal_glue_api_server.app import AmsdalGlueServerApp
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.services.commands import SchemaCommandService
from amsdal_glue_core.common.services.managers.connection import ConnectionManager
from amsdal_glue_core.containers import Container
from amsdal_glue_sql_parser.parsers.base import SqlParserBase
from amsdal_glue_sql_parser.parsers.sqloxide_parser import SqlOxideParser
from fastapi.testclient import TestClient


@pytest.fixture(scope='function')
def _register_connections() -> Generator[Any, Any, Any]:
    init_default_containers()
    Container.services.register(SqlParserBase, SqlOxideParser)

    with tempfile.TemporaryDirectory() as tmp_dir:
        db1 = DefaultConnectionPool(
            SqliteConnection,
            db_path=f'{tmp_dir}/db_name_1.sqlite3',
            check_same_thread=False,
        )
        db2 = DefaultConnectionPool(
            SqliteConnection,
            db_path=f'{tmp_dir}/db_name_2.sqlite3',
            check_same_thread=False,
        )
        db3 = DefaultConnectionPool(
            SqliteConnection,
            db_path=f'{tmp_dir}/db_name_3.sqlite3',
            check_same_thread=False,
        )

        connection_mng = Container.managers.get(ConnectionManager)
        connection_mng.register_connection_pool(db1)
        connection_mng.register_connection_pool(db1, schema_name='orders')
        connection_mng.register_connection_pool(db2, schema_name='cart')
        connection_mng.register_connection_pool(db3, schema_name='logs')

        yield


@pytest.fixture(scope='function', autouse=True)
def create_schemas(_register_connections) -> None:
    customers_schema = Schema(
        name='customers',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='customer_id',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='name',
                type=str,
                required=True,
            ),
            PropertySchema(
                name='email',
                type=str,
                required=True,
            ),
        ],
        constraints=[
            PrimaryKeyConstraint(name='pk_customers', fields=['customer_id']),
        ],
    )
    profile_schema = Schema(
        name='profile',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='profile_id',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='customer_id',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='address',
                type=str,
                required=True,
            ),
            PropertySchema(
                name='phone',
                type=str,
                required=True,
            ),
        ],
        constraints=[
            ForeignKeyConstraint(
                name='customer_fk',
                fields=['customer_id'],
                reference_schema=SchemaReference(name='customers', version=Version.LATEST),
                reference_fields=['customer_id'],
            ),
        ],
    )
    products_schema = Schema(
        name='products',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='product_id',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='name',
                type=str,
                required=True,
            ),
            PropertySchema(
                name='price',
                type=float,
                required=True,
            ),
        ],
        constraints=[
            PrimaryKeyConstraint(name='pk_products', fields=['product_id']),
        ],
    )
    orders_schema = Schema(
        name='orders',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='order_id',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='customer_id',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='product_id',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='quantity',
                type=int,
                required=True,
            ),
        ],
        constraints=[
            PrimaryKeyConstraint(name='pk_orders', fields=['order_id']),
            CheckConstraint(
                name='ck_quantity',
                condition=Conditions(
                    Condition(
                        field=FieldReference(field=Field(name='quantity'), table_name='orders'),
                        lookup=FieldLookup.GT,
                        value=Value(0),
                    ),
                ),
            ),
            UniqueConstraint(name='uk_orders', fields=['customer_id', 'product_id']),
        ],
    )
    cart_schema = Schema(
        name='cart',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='customer_id',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='product_id',
                type=int,
                required=True,
            ),
            PropertySchema(
                name='quantity',
                type=int,
                required=True,
            ),
        ],
        constraints=[
            PrimaryKeyConstraint(name='pk_cart', fields=['customer_id', 'product_id']),
        ],
    )
    logs_schema = Schema(
        name='logs',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='message',
                type=str,
                required=True,
            ),
            PropertySchema(
                name='created_at',
                type=datetime.datetime,
                required=True,
            ),
        ],
    )

    service = Container.services.get(SchemaCommandService)
    service.execute(
        SchemaCommand(mutations=[RegisterSchema(schema=customers_schema)]),
    )
    service.execute(
        SchemaCommand(mutations=[RegisterSchema(schema=profile_schema)]),
    )
    service.execute(
        SchemaCommand(mutations=[RegisterSchema(schema=products_schema)]),
    )
    service.execute(
        SchemaCommand(mutations=[RegisterSchema(schema=orders_schema)]),
    )
    service.execute(
        SchemaCommand(mutations=[RegisterSchema(schema=cart_schema)]),
    )
    service.execute(
        SchemaCommand(mutations=[RegisterSchema(schema=logs_schema)]),
    )


@pytest.fixture(scope='function')
def test_client() -> TestClient:
    amsdal_glue_app = AmsdalGlueServerApp()
    amsdal_glue_app.register_routes()

    return TestClient(amsdal_glue_app.app)
