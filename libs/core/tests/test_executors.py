from collections.abc import Iterator

import pytest

from amsdal_glue_core.commands.executors.data_command_executor import AsyncDataCommandNodeExecutor
from amsdal_glue_core.commands.executors.data_command_executor import DataCommandNodeExecutor
from amsdal_glue_core.commands.executors.schema_command_executor import AsyncSchemaCommandNodeExecutor
from amsdal_glue_core.commands.executors.schema_command_executor import SchemaCommandNodeExecutor
from amsdal_glue_core.commands.executors.transaction_command_executor import AsyncTransactionNodeExecutor
from amsdal_glue_core.commands.executors.transaction_command_executor import TransactionNodeExecutor
from amsdal_glue_core.commands.mutation_nodes import DataMutationNode
from amsdal_glue_core.commands.mutation_nodes import SchemaCommandNode
from amsdal_glue_core.commands.transaction_node import ExecutionTransactionCommandNode
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import TransactionAction
from amsdal_glue_core.common.interfaces.connection_manager import AsyncConnectionManager
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.containers import Container
from tests.conftest import DEFAULT_SCHEMA_NAME
from tests.conftest import MockAsyncConnectionManager
from tests.conftest import MockConnectionManager


@pytest.fixture(autouse=True)
def _register_mocks(
    mock_connection_manager: MockConnectionManager,
    mock_async_connection_manager: MockAsyncConnectionManager,
) -> Iterator[None]:
    try:
        Container.managers.register(ConnectionManager, mock_connection_manager)  # type: ignore[type-abstract]
        Container.managers.register(AsyncConnectionManager, mock_async_connection_manager)  # type: ignore[type-abstract]
        yield
    finally:
        Container.__sub_containers__.clear()


def test_data_command_executor(mock_connection_manager: MockConnectionManager) -> None:
    data_mutation_node = DataMutationNode(
        mutations=[InsertData(schema=SchemaReference(name=DEFAULT_SCHEMA_NAME), data=[Data(data={'key': 'value'})])]
    )
    DataCommandNodeExecutor().execute(data_mutation_node, transaction_id=None, lock_id=None)

    mock_connection_manager.connection_pool.connection.run_mutations.assert_called_once_with(
        data_mutation_node.mutations
    )


async def test_async_data_command_executor(mock_async_connection_manager: MockAsyncConnectionManager) -> None:
    data_mutation_node = DataMutationNode(
        mutations=[InsertData(schema=SchemaReference(name=DEFAULT_SCHEMA_NAME), data=[Data(data={'key': 'value'})])]
    )
    await AsyncDataCommandNodeExecutor().execute(data_mutation_node, transaction_id=None, lock_id=None)

    mock_async_connection_manager.connection_pool.connection.run_mutations.assert_called_once_with(
        data_mutation_node.mutations
    )


def test_schema_command_executor(mock_connection_manager: MockConnectionManager) -> None:
    schema_mutation_node = SchemaCommandNode(
        command=SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema=Schema(name=DEFAULT_SCHEMA_NAME, version='', properties=[]),
                )
            ]
        )
    )
    SchemaCommandNodeExecutor().execute(schema_mutation_node, transaction_id=None, lock_id=None)

    mock_connection_manager.connection_pool.connection.run_schema_command.assert_called_once_with(
        schema_mutation_node.command
    )


async def test_async_schema_command_executor(mock_async_connection_manager: MockAsyncConnectionManager) -> None:
    schema_mutation_node = SchemaCommandNode(
        command=SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema=Schema(name=DEFAULT_SCHEMA_NAME, version='', properties=[]),
                )
            ]
        )
    )
    await AsyncSchemaCommandNodeExecutor().execute(schema_mutation_node, transaction_id=None, lock_id=None)

    mock_async_connection_manager.connection_pool.connection.run_schema_command.assert_called_once_with(
        schema_mutation_node.command
    )


def test_transaction_command_executor(mock_connection_manager: MockConnectionManager) -> None:
    schema = SchemaReference(name=DEFAULT_SCHEMA_NAME)

    begin_transaction_node = ExecutionTransactionCommandNode(
        command=TransactionCommand(action=TransactionAction.BEGIN, schema=schema)
    )
    TransactionNodeExecutor().execute(begin_transaction_node, transaction_id=None, lock_id=None)
    mock_connection_manager.connection_pool.connection.begin_transaction.assert_called_once_with(
        begin_transaction_node.command
    )

    commit_transaction_node = ExecutionTransactionCommandNode(
        command=TransactionCommand(action=TransactionAction.COMMIT, schema=schema)
    )
    TransactionNodeExecutor().execute(commit_transaction_node, transaction_id=None, lock_id=None)
    mock_connection_manager.connection_pool.connection.commit_transaction.assert_called_once_with(
        commit_transaction_node.command
    )

    rollback_transaction_node = ExecutionTransactionCommandNode(
        command=TransactionCommand(action=TransactionAction.ROLLBACK, schema=schema)
    )
    TransactionNodeExecutor().execute(rollback_transaction_node, transaction_id=None, lock_id=None)
    mock_connection_manager.connection_pool.connection.rollback_transaction.assert_called_once_with(
        rollback_transaction_node.command
    )

    revert_transaction_node = ExecutionTransactionCommandNode(
        command=TransactionCommand(action=TransactionAction.REVERT, schema=schema)
    )
    TransactionNodeExecutor().execute(revert_transaction_node, transaction_id=None, lock_id=None)
    mock_connection_manager.connection_pool.connection.revert_transaction.assert_called_once_with(
        revert_transaction_node.command
    )


async def test_async_transaction_command_executor(mock_async_connection_manager: MockAsyncConnectionManager) -> None:
    schema = SchemaReference(name=DEFAULT_SCHEMA_NAME)

    begin_transaction_node = ExecutionTransactionCommandNode(
        command=TransactionCommand(action=TransactionAction.BEGIN, schema=schema)
    )
    await AsyncTransactionNodeExecutor().execute(begin_transaction_node, transaction_id=None, lock_id=None)
    mock_async_connection_manager.connection_pool.connection.begin_transaction.assert_called_once_with(
        begin_transaction_node.command
    )

    commit_transaction_node = ExecutionTransactionCommandNode(
        command=TransactionCommand(action=TransactionAction.COMMIT, schema=schema)
    )
    await AsyncTransactionNodeExecutor().execute(commit_transaction_node, transaction_id=None, lock_id=None)
    mock_async_connection_manager.connection_pool.connection.commit_transaction.assert_called_once_with(
        commit_transaction_node.command
    )

    rollback_transaction_node = ExecutionTransactionCommandNode(
        command=TransactionCommand(action=TransactionAction.ROLLBACK, schema=schema)
    )
    await AsyncTransactionNodeExecutor().execute(rollback_transaction_node, transaction_id=None, lock_id=None)
    mock_async_connection_manager.connection_pool.connection.rollback_transaction.assert_called_once_with(
        rollback_transaction_node.command
    )

    revert_transaction_node = ExecutionTransactionCommandNode(
        command=TransactionCommand(action=TransactionAction.REVERT, schema=schema)
    )
    await AsyncTransactionNodeExecutor().execute(revert_transaction_node, transaction_id=None, lock_id=None)
    mock_async_connection_manager.connection_pool.connection.revert_transaction.assert_called_once_with(
        revert_transaction_node.command
    )
