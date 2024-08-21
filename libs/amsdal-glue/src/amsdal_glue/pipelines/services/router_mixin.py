from typing import Any

from amsdal_glue.pipelines.containers import Pipeline


class ServiceRouter:
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        from amsdal_glue_core.containers import Container

        service_type = Container.services.get_dependency_type(self)
        pipeline = Pipeline().iter_container(service_type)
        first_container = next(pipeline)
        service = first_container.services.get(service_type)
        result = service.execute(*args, **kwargs)

        for container in pipeline:
            service = container.services.get(service_type)
            service.execute(*args, **kwargs)

        return result
