from amsdal_glue_core.common.data_models.results.schema import SchemaResult
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation
from amsdal_glue_core.common.services.queries import SchemaQueryService
from amsdal_glue_core.queries.planner.schema_query_planner import SchemaQueryPlanner


class DefaultSchemaQueryService(SchemaQueryService):
    def execute(self, query_op: SchemaQueryOperation) -> SchemaResult:
        from amsdal_glue_core.containers import Container

        _schema_query_planner = Container.planners.get(SchemaQueryPlanner)
        plan = _schema_query_planner.plan_schema_query(query_op.filters)

        try:
            plan.execute(transaction_id=query_op.transaction_id, lock_id=query_op.lock_id)
        except Exception as exc:  # noqa: BLE001
            return SchemaResult(success=False, message=str(exc), exception=exc)

        _schemas = plan.final_task.result if plan.final_task else plan.tasks[-1].result

        return SchemaResult(success=True, schemas=_schemas)
