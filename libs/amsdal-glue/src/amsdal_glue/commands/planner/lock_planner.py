from amsdal_glue_core.commands.lock_command_node import ExecutionLockCommand
from amsdal_glue_core.commands.planner.lock_command_planner import LockCommandPlanner
from amsdal_glue_core.common.operations.commands import LockCommand
from amsdal_glue_core.common.workflows.chain import ChainTask

from amsdal_glue.commands.tasks.lock_tasks import LockCommandTask


class DefaultLockCommandPlanner(LockCommandPlanner):
    def plan_lock(self, command: LockCommand) -> ChainTask:
        return ChainTask(
            tasks=[
                LockCommandTask(
                    lock_command=ExecutionLockCommand(
                        lock_id=command.lock_id,
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
