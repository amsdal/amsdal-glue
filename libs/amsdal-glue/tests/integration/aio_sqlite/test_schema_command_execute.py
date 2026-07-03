# mypy: disable-error-code="type-abstract"
import tempfile
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY
from amsdal_glue_core.commands.planner.schema_command_planner import AsyncSchemaCommandPlanner
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.types import DictType
from amsdal_glue_core.common.data_models.types import NestedType
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.interfaces.connection_manager import AsyncConnectionManager
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation
from amsdal_glue_core.common.services.queries import AsyncSchemaQueryService
from amsdal_glue_core.containers import Container

from amsdal_glue.connections.connection_pool import DefaultAsyncConnectionPool
from amsdal_glue.initialize import init_default_containers


@pytest.fixture(autouse=True)
async def register_default_connection() -> AsyncGenerator[None, None]:
    init_default_containers()
    connection_mng = Container.managers.get(AsyncConnectionManager)

    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = f'{temp_dir}/data.sqlite'
        connection_mng.register_connection_pool(
            DefaultAsyncConnectionPool(AsyncSqliteConnection, db_path=Path(db_path), check_same_thread=False),
        )

        try:
            yield
        finally:
            await connection_mng.disconnect_all()


@pytest.mark.asyncio
async def test_create_schema(register_default_connection: None) -> None:  # noqa: ARG001
    connection_mng = Container.managers.get(AsyncConnectionManager)
    schema = Schema(
        name='user',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='id',
                type=ScalarType.INTEGER,
                required=True,
            ),
            PropertySchema(
                name='email',
                type=ScalarType.TEXT,
                required=True,
            ),
            PropertySchema(
                name='age',
                type=ScalarType.INTEGER,
                required=True,
            ),
            PropertySchema(
                name='first_name',
                type=ScalarType.TEXT,
                required=False,
            ),
            PropertySchema(
                name='last_name',
                type=ScalarType.TEXT,
                required=False,
            ),
        ],
        constraints=[
            PrimaryKeyConstraint(name='pk_user_custom_name', fields=['id']),
            UniqueConstraint(name='uk_user_email', fields=['email'], condition=None),
            UniqueConstraint(name='uk_user_email_last_name', fields=['email', 'last_name'], condition=None),
            CheckConstraint(
                name='ck_user_age',
                condition=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='age'), table_name='user')
                        ),
                        lookup=FieldLookup.GT,
                        right=Value(value=18),
                    ),
                ),
            ),
        ],
        indexes=[
            IndexSchema(name='idx_user_email', fields=[IndexField(name='first_name'), IndexField(name='last_name')]),
        ],
    )

    planner = Container.planners.get(AsyncSchemaCommandPlanner)
    plan = planner.plan_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema=schema,
                    schema_ref=SchemaReference(name='user', version=Version.LATEST),
                ),
            ],
        ),
    )
    await plan.execute(transaction_id=None, lock_id=None)

    conn = await connection_mng.get_connection_pool('user').get_connection()
    result = await conn.query_schema(
        query=QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
    )
    assert len(result) == 1
    _schema = result[0]
    assert _schema.name == 'user'
    assert {prop.name: prop.type for prop in _schema.properties} == {
        'id': ScalarType.INTEGER,
        'email': ScalarType.TEXT,
        'age': ScalarType.INTEGER,
        'first_name': ScalarType.TEXT,
        'last_name': ScalarType.TEXT,
    }
    query_service = Container.services.get(AsyncSchemaQueryService)
    schema_result = await query_service.execute(
        SchemaQueryOperation(query=QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))),
    )

    assert schema_result.schemas == [
        Schema(
            name='user',
            version=Version.LATEST,
            properties=[
                PropertySchema(
                    name='id',
                    type=ScalarType.INTEGER,
                    required=True,
                ),
                PropertySchema(
                    name='email',
                    type=ScalarType.TEXT,
                    required=True,
                ),
                PropertySchema(
                    name='age',
                    type=ScalarType.INTEGER,
                    required=True,
                ),
                PropertySchema(
                    name='first_name',
                    type=ScalarType.TEXT,
                    required=False,
                ),
                PropertySchema(
                    name='last_name',
                    type=ScalarType.TEXT,
                    required=False,
                ),
            ],
            constraints=[
                PrimaryKeyConstraint(name='pk_user_custom_name', fields=['id']),
                UniqueConstraint(name='uk_user_email', fields=['email'], condition=None),
                UniqueConstraint(name='uk_user_email_last_name', fields=['email', 'last_name'], condition=None),
            ],
            indexes=[
                IndexSchema(
                    name='idx_user_email',
                    fields=[
                        IndexField(name='first_name', direction=OrderDirection.ASC, op_class=None),
                        IndexField(name='last_name', direction=OrderDirection.ASC, op_class=None),
                    ],
                ),
            ],
        )
    ]


@pytest.mark.asyncio
async def test_create_schema_complex_types(register_default_connection: None) -> None:  # noqa: ARG001
    connection_mng = Container.managers.get(AsyncConnectionManager)
    schema = Schema(
        name='user',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='dictionary',
                type=DictType(key_type=ScalarType.TEXT, value_type=ScalarType.INTEGER),
                required=True,
            ),
            PropertySchema(
                name='nested_schema',
                type=NestedType(properties={'string': ScalarType.TEXT, 'integer': ScalarType.INTEGER}),
                required=True,
            ),
        ],
    )

    planner = Container.planners.get(AsyncSchemaCommandPlanner)
    plan = planner.plan_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema=schema,
                    schema_ref=SchemaReference(name='user', version=Version.LATEST),
                ),
            ],
        ),
    )
    await plan.execute(transaction_id=None, lock_id=None)

    conn = await connection_mng.get_connection_pool('user').get_connection()
    result = await conn.query_schema(
        query=QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
    )
    assert len(result) == 1
    _schema = result[0]
    assert _schema.name == 'user'
    assert {prop.name: prop.type for prop in _schema.properties} == {
        'dictionary': ScalarType.JSONB,
        'nested_schema': ScalarType.JSONB,
    }
