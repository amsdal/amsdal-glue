from typing import Any

from amsdal_glue.pipelines.manager import PipelineManager


class PipelineServiceMixin:
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        from amsdal_glue_core.containers import Container

        service_type = Container.services.get_dependency_type(self)
        pipeline = Container.managers.get(PipelineManager)
        workflow = pipeline.iter_container(service_type)
        first_container = next(workflow)

        with Container.switch(first_container.name):
            service = first_container.services.get(service_type)
            result = service.execute(*args, **kwargs)

        for container in workflow:
            with Container.switch(container.name):
                service = container.services.get(service_type)
                service.execute(*args, **kwargs)

        return result
