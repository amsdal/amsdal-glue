from amsdal_glue_core.common.data_models.results.data import DataResult
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.services.queries import DataQueryService
from amsdal_glue_core.queries.planner.data_query_planner import DataQueryPlanner


class DefaultDataQueryService(DataQueryService):
    def execute(self, query_op: DataQueryOperation) -> DataResult:
        from amsdal_glue_core.containers import Container

        _query_planner = Container.planners.get(DataQueryPlanner)
        plan = _query_planner.plan_data_query(query_op.query)

        try:
            plan.execute(transaction_id=query_op.transaction_id, lock_id=query_op.lock_id)
        except Exception as exc:  # noqa: BLE001
            return DataResult(success=False, message=str(exc), exception=exc)

        _data = plan.final_task.result if plan.final_task else plan.tasks[-1].result

        return DataResult(success=True, data=_data)
