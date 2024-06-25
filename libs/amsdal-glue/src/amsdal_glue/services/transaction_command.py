from amsdal_glue_core.commands.planner.transaction_command_planner import TransactionCommandPlanner
from amsdal_glue_core.common.data_models.results.data import TransactionResult
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.services.commands import TransactionCommandService


class DefaultTransactionCommandService(TransactionCommandService):
    def execute(self, command: TransactionCommand) -> TransactionResult:
        from amsdal_glue_core.containers import Container

        query_planner = Container.planners.get(TransactionCommandPlanner)
        plan = query_planner.plan_transaction(command)

        try:
            plan.execute(transaction_id=command.transaction_id, lock_id=command.lock_id)
        except Exception as e:  # noqa: BLE001
            return TransactionResult(success=False, message=str(e))

        return TransactionResult(success=True, result=plan.result)
