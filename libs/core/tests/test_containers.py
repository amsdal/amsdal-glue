import threading
from typing import Any

import pytest

from amsdal_glue_core.containers import Container


@pytest.fixture(autouse=True)
def _reset_container() -> None:
    Container.__sub_containers__.clear()


def switch_and_check(
    container_name: str,
    results: dict,
    execution_name: str,
    delay: float = 0.5,
    container_state: Any = None,
) -> None:
    if container_state is not None:
        Container.deserialize_state(container_state)

    with Container.switch(container_name):
        # Simulate context switch by yielding control
        threading.Event().wait(delay)
        results[execution_name] = Container.__current_container__


def test_container_switch_in_multithreading() -> None:
    Container.define_sub_container('cont-1')
    Container.define_sub_container('cont-2')
    results: dict[str, str] = {}

    thread_1 = threading.Thread(
        target=switch_and_check,
        args=('cont-1', results, 'thread_1'),
        kwargs={
            'delay': 0.5,
        },
    )
    thread_2 = threading.Thread(
        target=switch_and_check,
        args=('cont-2', results, 'thread_2'),
        kwargs={
            'delay': 1.0,
        },
    )

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

    assert results['thread_1'] == 'cont-1'
    assert results['thread_2'] == 'cont-2'


def test_container_switch_in_multiprocessing() -> None:
    import multiprocessing

    Container.define_sub_container('cont-1')
    Container.define_sub_container('cont-2')

    manager = multiprocessing.Manager()
    shared_dict = manager.dict()
    container_state = Container.serialize_state()

    process_1 = multiprocessing.Process(
        target=switch_and_check,
        args=('cont-1', shared_dict, 'process_1'),
        kwargs={
            'delay': 0.5,
            'container_state': container_state,
        },
    )
    process_2 = multiprocessing.Process(
        target=switch_and_check,
        args=('cont-2', shared_dict, 'process_2'),
        kwargs={
            'delay': 1.0,
            'container_state': container_state,
        },
    )

    process_1.start()
    process_2.start()

    process_1.join()
    process_2.join()

    assert shared_dict['process_1'] == 'cont-1'
    assert shared_dict['process_2'] == 'cont-2'
