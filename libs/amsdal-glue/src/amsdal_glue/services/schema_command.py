from amsdal_glue_core.commands.planner.schema_command_planner import SchemaCommandPlanner
from amsdal_glue_core.common.data_models.results.schema import SchemaResult
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.services.commands import SchemaCommandService


class DefaultSchemaCommandService(SchemaCommandService):
    """
    DefaultSchemaCommandService is responsible for executing schema commands.
    It extends the SchemaCommandService class.
    """

    def execute(self, command: SchemaCommand) -> SchemaResult:
        """
        Executes the given schema command.

        Args:
            command (SchemaCommand): The schema command to be executed.

        Returns:
            SchemaResult: The result of the schema command execution.
        """
        from amsdal_glue_core.containers import Container

        query_planner = Container.planners.get(SchemaCommandPlanner)
        plan = query_planner.plan_schema_command(command)

        try:
            plan.execute(transaction_id=command.root_transaction_id, lock_id=command.lock_id)
        except Exception as e:  # noqa: BLE001
            return SchemaResult(success=False, message=str(e))
        else:
            _schemas = plan.final_task.result if plan.final_task else plan.tasks[-1].result

        return SchemaResult(success=True, schemas=_schemas)
