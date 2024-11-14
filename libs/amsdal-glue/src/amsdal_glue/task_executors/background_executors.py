# mypy: disable-error-code="type-abstract"
import asyncio
from threading import Thread

from amsdal_glue_core.common.workflows.task import AsyncTask
from amsdal_glue_core.common.workflows.task import Task

from amsdal_glue.interfaces import AsyncSequentialExecutor
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

        def background_task(container_name: str | None):
            if container_name:
                with Container.switch(container_name):
                    for task in tasks:
                        task.execute(transaction_id=transaction_id, lock_id=lock_id)

                    if final_task is not None:
                        final_task.execute(transaction_id=transaction_id, lock_id=lock_id)
            else:
                for task in tasks:
                    task.execute(transaction_id=transaction_id, lock_id=lock_id)

                if final_task is not None:
                    final_task.execute(transaction_id=transaction_id, lock_id=lock_id)

        thread = Thread(target=background_task, args=(Container.__current_container__,))
        thread.start()
        self._threads.append(thread)

        with Container.root():
            runtime = Container.managers.get(RuntimeManager)
            runtime.add_shutdown_hook(self.shutdown)

    def shutdown(self):
        for thread in self._threads:
            thread.join()

        self._threads.clear()


class BackgroundAsyncSequentialExecutor(AsyncSequentialExecutor):
    def __init__(self):
        self._threads: list[Thread] = []

    async def execute_sequential(
        self,
        tasks: list[AsyncTask],
        final_task: AsyncTask | None,
        transaction_id: str | None,
        lock_id: str | None,
    ) -> None:
        from amsdal_glue import Container
        from amsdal_glue.interfaces import RuntimeManager

        def background_task(container_name: str | None):
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError as e:
                if str(e).startswith('There is no current event loop in thread'):
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                else:
                    raise

            if container_name:
                with Container.switch(container_name):
                    for task in tasks:
                        loop.run_until_complete(task.execute(transaction_id=transaction_id, lock_id=lock_id))

                    if final_task is not None:
                        loop.run_until_complete(final_task.execute(transaction_id=transaction_id, lock_id=lock_id))
            else:
                for task in tasks:
                    loop.run_until_complete(task.execute(transaction_id=transaction_id, lock_id=lock_id))

                if final_task is not None:
                    loop.run_until_complete(final_task.execute(transaction_id=transaction_id, lock_id=lock_id))

        thread = Thread(target=background_task, args=(Container.__current_container__,))
        thread.start()
        self._threads.append(thread)

        with Container.root():
            runtime = Container.managers.get(RuntimeManager)
            runtime.add_shutdown_hook(self.shutdown)

    def shutdown(self):
        for thread in self._threads:
            thread.join()

        self._threads.clear()
