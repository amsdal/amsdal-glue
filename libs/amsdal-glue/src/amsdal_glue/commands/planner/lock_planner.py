from amsdal_glue_core.commands.lock_command_node import ExecutionLockCommand
from amsdal_glue_core.commands.planner.lock_command_planner import AsyncLockCommandPlanner
from amsdal_glue_core.commands.planner.lock_command_planner import LockCommandPlanner
from amsdal_glue_core.common.operations.commands import LockCommand
from amsdal_glue_core.common.workflows.chain import AsyncChainTask
from amsdal_glue_core.common.workflows.chain import ChainTask

from amsdal_glue.commands.tasks.lock_tasks import AsyncLockCommandTask
from amsdal_glue.commands.tasks.lock_tasks import LockCommandTask


class DefaultLockCommandPlanner(LockCommandPlanner):
    """
    DefaultLockCommandPlanner is responsible for planning lock commands by creating a chain of tasks
    that execute lock operations. It extends the LockCommandPlanner class.
    """

    def plan_lock(self, command: LockCommand) -> ChainTask:
        """
        Plans the execution of a lock command by creating a chain of tasks.

        Args:
            command (LockCommand): The lock command containing lock operations to be executed.

        Returns:
            ChainTask: A chain of tasks that execute the lock operations.
        """
        return ChainTask(
            tasks=[
                LockCommandTask(
                    lock_command=ExecutionLockCommand(
                        lock_id=command.lock_id,
                        root_transaction_id=command.root_transaction_id,
                        transaction_id=command.transaction_id,
                        action=command.action,
                        mode=command.mode,
                        parameter=command.parameter,
                        locked_object=lock_object,
                    )
                )
                for lock_object in command.locked_objects
            ]
        )


class DefaultAsyncLockCommandPlanner(AsyncLockCommandPlanner):
    """
    DefaultAsyncLockCommandPlanner is responsible for planning lock commands by creating a chain of tasks
    that execute lock operations. It extends the AsyncLockCommandPlanner class.
    """

    def plan_lock(self, command: LockCommand) -> AsyncChainTask:
        """
        Plans the execution of a lock command by creating a chain of tasks.

        Args:
            command (LockCommand): The lock command containing lock operations to be executed.

        Returns:
            AsyncChainTask: A chain of tasks that execute the lock operations.
        """
        return AsyncChainTask(
            tasks=[
                AsyncLockCommandTask(
                    lock_command=ExecutionLockCommand(
                        lock_id=command.lock_id,
                        root_transaction_id=command.root_transaction_id,
                        transaction_id=command.transaction_id,
                        action=command.action,
                        mode=command.mode,
                        parameter=command.parameter,
                        locked_object=lock_object,
                    )
                )
                for lock_object in command.locked_objects
            ]
        )
