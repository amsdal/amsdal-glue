# mypy: disable-error-code="type-abstract"
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_core.commands.planner.data_command_planner import DataCommandPlanner
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.mutations.data import DeleteData
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateData
from amsdal_glue_core.containers import Container

from amsdal_glue.connections.connection_pool import DefaultConnectionPool
from amsdal_glue.initialize import init_default_containers


@pytest.fixture(autouse=True)
def _register_default_connection() -> Generator[None, None, None]:
    init_default_containers()
    connection_mng = Container.managers.get(ConnectionManager)

    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = f'{temp_dir}/data.sqlite'
        connection_mng.register_connection_pool(
            DefaultConnectionPool(SqliteConnection, db_path=Path(db_path), check_same_thread=False),
            schema_name='shippings',
        )

        connection_mng.get_connection_pool('shippings').get_connection().execute(  # type: ignore[attr-defined]
            'CREATE TABLE IF NOT EXISTS shippings (id TEXT, customer_id TEXT, status TEXT)'
        )

        try:
            yield
        finally:
            connection_mng.disconnect_all()


def test_insert_data_single_element() -> None:
    connection_mng = Container.managers.get(ConnectionManager)
    query = DataCommand(
        lock_id=None,
        transaction_id=None,
        mutations=[
            InsertData(
                schema=SchemaReference(name='shippings', version=Version.LATEST),
                data=[
                    Data(
                        data={'id': '111', 'customer_id': '1', 'status': 'shipped'},
                    )
                ],
            )
        ],
    )
    planner = Container.planners.get(DataCommandPlanner)
    plan = planner.plan_data_command(query)

    plan.execute(transaction_id=None, lock_id=None)
    assert len(plan.tasks) == 1
    assert plan.tasks[0].item.mutations == [query.mutations[0]]

    assert plan.tasks[0].result == [None]

    assert (
        connection_mng.get_connection_pool('shippings')  # type: ignore[attr-defined]
        .get_connection()
        .execute('SELECT id, customer_id, status FROM shippings')
        .fetchall()
        == [('111', '1', 'shipped')]
    )


def test_update_data_single_element() -> None:
    connection_mng = Container.managers.get(ConnectionManager)
    connection_mng.get_connection_pool('shippings').get_connection().execute(  # type: ignore[attr-defined]
        'INSERT INTO shippings (id, customer_id, status) '
        'VALUES ("111", "1", "shipped"), ("222", "2", "shipped"), ("333", "3", "shipped")'
    )
    query = DataCommand(
        lock_id=None,
        transaction_id=None,
        mutations=[
            UpdateData(
                schema=SchemaReference(name='shippings', version=Version.LATEST, alias='s'),
                data=Data(
                    data={'id': '111', 'customer_id': '1', 'status': 'cancelled'},
                ),
                query=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='customer_id'), table_name='s')
                        ),
                        lookup=FieldLookup.EQ,
                        right=Value(value='1'),
                    ),
                ),
            )
        ],
    )

    planner = Container.planners.get(DataCommandPlanner)
    plan = planner.plan_data_command(query)

    plan.execute(transaction_id=None, lock_id=None)
    assert len(plan.tasks) == 1
    assert plan.tasks[0].item.mutations == [query.mutations[0]]

    assert plan.tasks[0].result == [None]

    assert connection_mng.get_connection_pool('shippings').get_connection().execute(  # type: ignore[attr-defined]
        'SELECT id, customer_id, status FROM shippings ORDER BY id'
    ).fetchall() == [
        ('111', '1', 'cancelled'),
        ('222', '2', 'shipped'),
        ('333', '3', 'shipped'),
    ]


def test_delete_data_single_element() -> None:
    connection_mng = Container.managers.get(ConnectionManager)
    connection_mng.get_connection_pool('shippings').get_connection().execute(  # type: ignore[attr-defined]
        'INSERT INTO shippings (id, customer_id, status) '
        'VALUES ("111", "1", "shipped"), ("222", "2", "shipped"), ("333", "3", "shipped")'
    )
    query = DataCommand(
        lock_id=None,
        transaction_id=None,
        mutations=[
            DeleteData(
                schema=SchemaReference(name='shippings', version=Version.LATEST, alias='s'),
                query=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='customer_id'), table_name='s')
                        ),
                        lookup=FieldLookup.EQ,
                        right=Value(value='1'),
                    ),
                ),
            )
        ],
    )

    planner = Container.planners.get(DataCommandPlanner)
    plan = planner.plan_data_command(query)

    plan.execute(transaction_id=None, lock_id=None)
    assert len(plan.tasks) == 1
    assert plan.tasks[0].item.mutations == [query.mutations[0]]

    assert plan.tasks[0].result == [None]

    assert connection_mng.get_connection_pool('shippings').get_connection().execute(  # type: ignore[attr-defined]
        'SELECT id, customer_id, status FROM shippings ORDER BY id'
    ).fetchall() == [
        ('222', '2', 'shipped'),
        ('333', '3', 'shipped'),
    ]


def test_create_and_update_data_single_element() -> None:
    connection_mng = Container.managers.get(ConnectionManager)
    query = DataCommand(
        lock_id=None,
        transaction_id=None,
        mutations=[
            InsertData(
                schema=SchemaReference(name='shippings', version=Version.LATEST),
                data=[
                    Data(
                        data={'id': '111', 'customer_id': '1', 'status': 'shipped'},
                    )
                ],
            ),
            UpdateData(
                schema=SchemaReference(name='shippings', version=Version.LATEST, alias='s'),
                data=Data(
                    data={'id': '111', 'customer_id': '1', 'status': 'cancelled'},
                ),
                query=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='customer_id'), table_name='s')
                        ),
                        lookup=FieldLookup.EQ,
                        right=Value(value='1'),
                    ),
                ),
            ),
        ],
    )

    planner = Container.planners.get(DataCommandPlanner)
    plan = planner.plan_data_command(query)

    plan.execute(transaction_id=None, lock_id=None)
    assert len(plan.tasks) == 1
    assert plan.tasks[0].item.mutations == [query.mutations[0], query.mutations[1]]

    assert plan.tasks[0].result == [None, None]

    assert connection_mng.get_connection_pool('shippings').get_connection().execute(  # type: ignore[attr-defined]
        'SELECT id, customer_id, status FROM shippings'
    ).fetchall() == [
        ('111', '1', 'cancelled'),
    ]


def test_create_and_delete_data_single_element() -> None:
    connection_mng = Container.managers.get(ConnectionManager)
    query = DataCommand(
        lock_id=None,
        transaction_id=None,
        mutations=[
            InsertData(
                schema=SchemaReference(name='shippings', version=Version.LATEST),
                data=[
                    Data(
                        data={'id': '111', 'customer_id': '1', 'status': 'shipped'},
                    )
                ],
            ),
            DeleteData(
                schema=SchemaReference(name='shippings', version=Version.LATEST, alias='s'),
                query=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='customer_id'), table_name='s')
                        ),
                        lookup=FieldLookup.EQ,
                        right=Value(value='1'),
                    ),
                ),
            ),
        ],
    )

    planner = Container.planners.get(DataCommandPlanner)
    plan = planner.plan_data_command(query)

    plan.execute(transaction_id=None, lock_id=None)
    assert len(plan.tasks) == 1
    assert plan.tasks[0].item.mutations == [query.mutations[0], query.mutations[1]]

    assert plan.tasks[0].result == [None, None]

    assert (
        connection_mng.get_connection_pool('shippings')  # type: ignore[attr-defined]
        .get_connection()
        .execute('SELECT id, customer_id, status FROM shippings')
        .fetchall()
        == []
    )


def test_create_multiple_data_elements() -> None:
    connection_mng = Container.managers.get(ConnectionManager)
    query = DataCommand(
        lock_id=None,
        transaction_id=None,
        mutations=[
            InsertData(
                schema=SchemaReference(name='shippings', version=Version.LATEST),
                data=[
                    Data(
                        data={'id': '111', 'customer_id': '1', 'status': 'shipped'},
                    ),
                    Data(
                        data={'id': '222', 'customer_id': '2', 'status': 'shipped'},
                    ),
                    Data(
                        data={'id': '333', 'customer_id': '3', 'status': 'shipped'},
                    ),
                ],
            )
        ],
    )
    planner = Container.planners.get(DataCommandPlanner)
    plan = planner.plan_data_command(query)

    plan.execute(transaction_id=None, lock_id=None)
    assert len(plan.tasks) == 1
    assert plan.tasks[0].item.mutations == [query.mutations[0]]

    assert plan.tasks[0].result == [None]

    assert connection_mng.get_connection_pool('shippings').get_connection().execute(  # type: ignore[attr-defined]
        'SELECT id, customer_id, status FROM shippings ORDER BY id'
    ).fetchall() == [
        ('111', '1', 'shipped'),
        ('222', '2', 'shipped'),
        ('333', '3', 'shipped'),
    ]
