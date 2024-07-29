from amsdal_glue_core.commands.planner.data_command_planner import DataCommandPlanner
from amsdal_glue_core.common.data_models.results.data import DataResult
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.services.commands import DataCommandService


class DefaultDataCommandService(DataCommandService):
    """
    DefaultDataCommandService is responsible for executing data commands.
    It extends the DataCommandService class.
    """

    def execute(self, command: DataCommand) -> DataResult:
        """
        Executes the given data command.

        Args:
            command (DataCommand): The data command to be executed.

        Returns:
            DataResult: The result of the data command execution.
        """
        from amsdal_glue_core.containers import Container

        query_planner = Container.planners.get(DataCommandPlanner)
        plan = query_planner.plan_data_command(command)

        try:
            plan.execute(transaction_id=command.root_transaction_id, lock_id=command.lock_id)
        except Exception as e:  # noqa: BLE001
            return DataResult(success=False, message=str(e))
        else:
            _data = plan.final_task.result if plan.final_task else plan.tasks[-1].result

        return DataResult(success=True, data=_data)
