import pytest
from src.models import Task, TaskStatus
from src.queue import TaskQueue


@pytest.fixture
def filled_queue():
    q = TaskQueue()
    q.add_task(Task(id=1, name="low", priority=1, payload="meow"))
    q.add_task(Task(id=2, name="high", priority=9, payload="meow"))
    q.add_task(Task(id=3, name="mid", priority=5, payload="meow"))
    return q


def test_queue_iteration(filled_queue):
    items = []
    for task in filled_queue:
        items.append(task)
    assert len(items) == 3
    assert items[0].id == 1


def test_queue_repeatable_iteration(filled_queue):
    first_pass = list(filled_queue)
    second_pass = list(filled_queue)
    assert len(first_pass) == len(second_pass) == 3
    assert first_pass == second_pass


def test_filter_by_status(filled_queue):
    result = filled_queue.filter_by_status(TaskStatus.CREATED)
    assert not isinstance(result, list)
    assert hasattr(result, "__next__") or hasattr(result, "__iter__")
    assert len(list(result)) == 3


def test_filter_by_priority(filled_queue):
    urgent = list(filled_queue.filter_by_priority(8))
    assert len(urgent) == 1
    assert urgent[0].id == 2


def test_stop_iteration(filled_queue):
    it = iter(filled_queue.filter_by_priority(10))
    with pytest.raises(StopIteration):
        next(it)


def test_queue_len(filled_queue):
    assert len(filled_queue) == 3

@pytest.mark.asyncio
async def test_load_from_source():
    class MockSource:
        async def get_tasks(self):
            return [
                Task(id=5, name="From Obj", payload="...", priority=1),
                Task(id=5, name="From Obj", payload="...", priority=1),
                Task(id=5, name="From Obj", payload="...", priority=1)
            ]

    q = TaskQueue()
    await q.load_from_source(MockSource())
    assert len(q) == 3
    assert all(isinstance(t, Task) for t in q)