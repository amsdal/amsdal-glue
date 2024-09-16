from threading import Thread

from amsdal_glue_core.common.workflows.task import Task

from amsdal_glue.interfaces import SequentialExecutor


class BackgroundSequentialExecutor(SequentialExecutor):
    def __init__(self):
        self._threads: list[Thread] = []

    def execute_sequential(
        self,
        tasks: list[Task],
        final_task: Task | None,
        transaction_id: str | None,
        lock_id: str | None,
    ) -> None:
        from amsdal_glue import Container
        from amsdal_glue.interfaces import RuntimeManager

        def background_task():
            for task in tasks:
                task.execute(transaction_id=transaction_id, lock_id=lock_id)

            if final_task is not None:
                final_task.execute(transaction_id=transaction_id, lock_id=lock_id)

        thread = Thread(target=background_task)
        thread.start()
        self._threads.append(thread)

        with Container.root():
            runtime = Container.managers.get(RuntimeManager)
            runtime.add_shutdown_hook(self.shutdown)

    def shutdown(self):
        for thread in self._threads:
            thread.join()

        self._threads.clear()
