from amsdal_glue_core.commands.planner.schema_command_planner import SchemaCommandPlanner
from amsdal_glue_core.common.data_models.results.schema import SchemaResult
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.services.commands import SchemaCommandService


class DefaultSchemaCommandService(SchemaCommandService):
    def execute(self, command: SchemaCommand) -> SchemaResult:
        from amsdal_glue_core.containers import Container

        query_planner = Container.planners.get(SchemaCommandPlanner)
        plan = query_planner.plan_schema_command(command)

        try:
            plan.execute()
        except Exception as e:  # noqa: BLE001
            return SchemaResult(success=False, message=str(e))
        else:
            _schema = plan.final_task.result if plan.final_task else plan.tasks[-1].result

        return SchemaResult(success=True, schema=_schema)
