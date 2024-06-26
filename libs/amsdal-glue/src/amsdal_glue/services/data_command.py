from amsdal_glue_core.commands.planner.data_command_planner import DataCommandPlanner
from amsdal_glue_core.common.data_models.results.data import DataResult
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.services.commands import DataCommandService


class DefaultDataCommandService(DataCommandService):
    def execute(self, command: DataCommand) -> DataResult:
        from amsdal_glue_core.containers import Container

        query_planner = Container.planners.get(DataCommandPlanner)
        plan = query_planner.plan_data_command(command)

        try:
            plan.execute(transaction_id=command.transaction_id, lock_id=command.lock_id)
        except Exception as e:  # noqa: BLE001
            return DataResult(success=False, message=str(e))
        else:
            _data = plan.final_task.result if plan.final_task else plan.tasks[-1].result

        return DataResult(success=True, data=_data)
