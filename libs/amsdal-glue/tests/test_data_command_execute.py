# mypy: disable-error-code="type-abstract"
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from amsdal_glue.initialize import init_default_containers
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_core.commands.planner.data_command_planner import DataCommandPlanner
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.metadata import Metadata
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.helpers.singleton import Singleton
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.mutations.data import DeleteData
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateData
from amsdal_glue_core.common.services.managers.connection import ConnectionManager
from amsdal_glue_core.containers import Container


@pytest.fixture(autouse=True)
def _register_default_connection() -> Generator[None, None, None]:
    init_default_containers()
    connection_mng = Container.managers.get(ConnectionManager)

    shipping_connection = SqliteConnection()
    connection_mng.register_connection(shipping_connection, schema_name='shippings')

    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = f'{temp_dir}/data.sqlite'
        shipping_connection.connect(db_path=Path(db_path), check_same_thread=False)
        shipping_connection.execute('CREATE TABLE IF NOT EXISTS shippings (id TEXT, customer_id TEXT, status TEXT)')

        yield

    shipping_connection.disconnect()
    Singleton.invalidate_all_instances()


def test_insert_data_single_element() -> None:
    query = DataCommand(
        lock_id=None,
        transaction_id=None,
        mutations=[
            InsertData(
                schema=SchemaReference(name='shippings', version=Version.LATEST),
                data=[
                    Data(
                        data={'id': '111', 'customer_id': '1', 'status': 'shipped'},
                        metadata=Metadata(
                            object_id='1',
                            object_version='1',
                            created_at='2021-01-01T00:00:00Z',
                            updated_at='2021-01-01T00:00:00Z',
                        ),
                    )
                ],
            )
        ],
    )
    planner = Container.planners.get(DataCommandPlanner)
    plan = planner.plan_data_command(query)

    plan.execute()
    assert len(plan.tasks) == 1
    assert plan.tasks[0].item.mutations == [query.mutations[0]]

    assert plan.tasks[0].result == [None]

    assert (
        [('111', '1', 'shipped')]
        == ConnectionManager()  # type: ignore[attr-defined]
        .get_connection('shippings')
        .execute('SELECT id, customer_id, status FROM shippings')
        .fetchall()
    )


def test_update_data_single_element() -> None:
    ConnectionManager().get_connection('shippings').execute(  # type: ignore[attr-defined]
        'INSERT INTO shippings (id, customer_id, status) '
        'VALUES ("111", "1", "shipped"), ("222", "2", "shipped"), ("333", "3", "shipped")'
    )
    query = DataCommand(
        lock_id=None,
        transaction_id=None,
        mutations=[
            UpdateData(
                schema=SchemaReference(name='shippings', version=Version.LATEST, alias='s'),
                data=[
                    Data(
                        data={'id': '111', 'customer_id': '1', 'status': 'cancelled'},
                        metadata=Metadata(
                            object_id='1',
                            object_version='1',
                            created_at='2021-01-01T00:00:00Z',
                            updated_at='2021-01-01T00:00:00Z',
                        ),
                    )
                ],
                query=Conditions(
                    Condition(
                        field=FieldReference(field=Field(name='customer_id'), table_name='s'),
                        lookup=FieldLookup.EQ,
                        value=Value(value='1'),
                    ),
                ),
            )
        ],
    )

    planner = Container.planners.get(DataCommandPlanner)
    plan = planner.plan_data_command(query)

    plan.execute()
    assert len(plan.tasks) == 1
    assert plan.tasks[0].item.mutations == [query.mutations[0]]

    assert plan.tasks[0].result == [None]

    assert [
        ('111', '1', 'cancelled'),
        ('222', '2', 'shipped'),
        ('333', '3', 'shipped'),
    ] == ConnectionManager().get_connection('shippings').execute(  # type: ignore[attr-defined]
        'SELECT id, customer_id, status FROM shippings ORDER BY id'
    ).fetchall()


def test_delete_data_single_element() -> None:
    ConnectionManager().get_connection('shippings').execute(  # type: ignore[attr-defined]
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
                        field=FieldReference(field=Field(name='customer_id'), table_name='s'),
                        lookup=FieldLookup.EQ,
                        value=Value(value='1'),
                    ),
                ),
            )
        ],
    )

    planner = Container.planners.get(DataCommandPlanner)
    plan = planner.plan_data_command(query)

    plan.execute()
    assert len(plan.tasks) == 1
    assert plan.tasks[0].item.mutations == [query.mutations[0]]

    assert plan.tasks[0].result == [None]

    assert [
        ('222', '2', 'shipped'),
        ('333', '3', 'shipped'),
    ] == ConnectionManager().get_connection('shippings').execute(  # type: ignore[attr-defined]
        'SELECT id, customer_id, status FROM shippings ORDER BY id'
    ).fetchall()


def test_create_and_update_data_single_element() -> None:
    query = DataCommand(
        lock_id=None,
        transaction_id=None,
        mutations=[
            InsertData(
                schema=SchemaReference(name='shippings', version=Version.LATEST),
                data=[
                    Data(
                        data={'id': '111', 'customer_id': '1', 'status': 'shipped'},
                        metadata=Metadata(
                            object_id='1',
                            object_version='1',
                            created_at='2021-01-01T00:00:00Z',
                            updated_at='2021-01-01T00:00:00Z',
                        ),
                    )
                ],
            ),
            UpdateData(
                schema=SchemaReference(name='shippings', version=Version.LATEST, alias='s'),
                data=[
                    Data(
                        data={'id': '111', 'customer_id': '1', 'status': 'cancelled'},
                        metadata=Metadata(
                            object_id='1',
                            object_version='1',
                            created_at='2021-01-01T00:00:00Z',
                            updated_at='2021-01-01T00:00:00Z',
                        ),
                    )
                ],
                query=Conditions(
                    Condition(
                        field=FieldReference(field=Field(name='customer_id'), table_name='s'),
                        lookup=FieldLookup.EQ,
                        value=Value(value='1'),
                    ),
                ),
            ),
        ],
    )

    planner = Container.planners.get(DataCommandPlanner)
    plan = planner.plan_data_command(query)

    plan.execute()
    assert len(plan.tasks) == 1
    assert plan.tasks[0].item.mutations == [query.mutations[0], query.mutations[1]]

    assert plan.tasks[0].result == [None, None]

    assert [
        ('111', '1', 'cancelled'),
    ] == ConnectionManager().get_connection('shippings').execute(  # type: ignore[attr-defined]
        'SELECT id, customer_id, status FROM shippings'
    ).fetchall()


def test_create_and_delete_data_single_element() -> None:
    query = DataCommand(
        lock_id=None,
        transaction_id=None,
        mutations=[
            InsertData(
                schema=SchemaReference(name='shippings', version=Version.LATEST),
                data=[
                    Data(
                        data={'id': '111', 'customer_id': '1', 'status': 'shipped'},
                        metadata=Metadata(
                            object_id='1',
                            object_version='1',
                            created_at='2021-01-01T00:00:00Z',
                            updated_at='2021-01-01T00:00:00Z',
                        ),
                    )
                ],
            ),
            DeleteData(
                schema=SchemaReference(name='shippings', version=Version.LATEST, alias='s'),
                query=Conditions(
                    Condition(
                        field=FieldReference(field=Field(name='customer_id'), table_name='s'),
                        lookup=FieldLookup.EQ,
                        value=Value(value='1'),
                    ),
                ),
            ),
        ],
    )

    planner = Container.planners.get(DataCommandPlanner)
    plan = planner.plan_data_command(query)

    plan.execute()
    assert len(plan.tasks) == 1
    assert plan.tasks[0].item.mutations == [query.mutations[0], query.mutations[1]]

    assert plan.tasks[0].result == [None, None]

    assert (
        []
        == ConnectionManager()  # type: ignore[attr-defined]
        .get_connection('shippings')
        .execute('SELECT id, customer_id, status FROM shippings')
        .fetchall()
    )


def test_create_multiple_data_elements() -> None:
    query = DataCommand(
        lock_id=None,
        transaction_id=None,
        mutations=[
            InsertData(
                schema=SchemaReference(name='shippings', version=Version.LATEST),
                data=[
                    Data(
                        data={'id': '111', 'customer_id': '1', 'status': 'shipped'},
                        metadata=Metadata(
                            object_id='1',
                            object_version='1',
                            created_at='2021-01-01T00:00:00Z',
                            updated_at='2021-01-01T00:00:00Z',
                        ),
                    ),
                    Data(
                        data={'id': '222', 'customer_id': '2', 'status': 'shipped'},
                        metadata=Metadata(
                            object_id='2',
                            object_version='1',
                            created_at='2021-01-01T00:00:00Z',
                            updated_at='2021-01-01T00:00:00Z',
                        ),
                    ),
                    Data(
                        data={'id': '333', 'customer_id': '3', 'status': 'shipped'},
                        metadata=Metadata(
                            object_id='3',
                            object_version='1',
                            created_at='2021-01-01T00:00:00Z',
                            updated_at='2021-01-01T00:00:00Z',
                        ),
                    ),
                ],
            )
        ],
    )
    planner = Container.planners.get(DataCommandPlanner)
    plan = planner.plan_data_command(query)

    plan.execute()
    assert len(plan.tasks) == 1
    assert plan.tasks[0].item.mutations == [query.mutations[0]]

    assert plan.tasks[0].result == [None]

    assert [
        ('111', '1', 'shipped'),
        ('222', '2', 'shipped'),
        ('333', '3', 'shipped'),
    ] == ConnectionManager().get_connection('shippings').execute(  # type: ignore[attr-defined]
        'SELECT id, customer_id, status FROM shippings ORDER BY id'
    ).fetchall()