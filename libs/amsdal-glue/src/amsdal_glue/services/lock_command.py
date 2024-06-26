from amsdal_glue_core.commands.planner.lock_command_planner import LockCommandPlanner
from amsdal_glue_core.common.data_models.results.data import LockResult
from amsdal_glue_core.common.operations.commands import LockCommand
from amsdal_glue_core.common.services.commands import LockCommandService


class DefaultLockCommandService(LockCommandService):
    def execute(self, command: LockCommand) -> LockResult:
        from amsdal_glue_core.containers import Container

        query_planner = Container.planners.get(LockCommandPlanner)
        plan = query_planner.plan_lock(command)

        try:
            plan.execute(transaction_id=command.transaction_id, lock_id=command.lock_id)
        except Exception as e:  # noqa: BLE001
            return LockResult(success=False, message=str(e))

        return LockResult(success=True, result=plan.result)
