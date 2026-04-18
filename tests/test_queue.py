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


def test_queue_repeatable_iteratio(filled_queue):
    first = list(filled_queue)
    second = list(filled_queue)
    assert len(first) == len(second) == 3
    assert first == second

def test_parallel_iteration(filled_queue):
    it1 = iter(filled_queue)
    it2 = iter(filled_queue)
    next(it1)
    assert next(it2).id == 1
    assert next(it1).id == 2

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

@pytest.fixture
def queue_with_data():
    q = TaskQueue()
    t1 = Task(id=1, name="first", payload="...", priority=1)
    t2 = Task(id=2, name="second", payload="...", priority=2)
    t3 = Task(id=3, name="third", payload="...", priority=3)
    q.add_task(t1)
    q.add_task(t2)
    q.add_task(t3)
    return q

def test_queue_getitem(queue_with_data):
    assert queue_with_data[0].id == 1
    assert queue_with_data[-1].id == 3

    slice_result = queue_with_data[0:2]
    assert len(slice_result) == 2
    assert slice_result[1].id == 2


def test_queue_getitem_error(queue_with_data):
    with pytest.raises(IndexError):
        _ = queue_with_data[10]


def test_queue_contains_by_id(queue_with_data):
    assert 1 in queue_with_data
    assert 2 in queue_with_data
    assert 99 not in queue_with_data


def test_queue_contains_by_object(queue_with_data):
    existing_task = queue_with_data[0]
    new_task = Task(id=10, name="new", payload="...")

    assert existing_task in queue_with_data
    assert new_task not in queue_with_data


def test_queue_clear(queue_with_data):
    assert len(queue_with_data) == 3
    queue_with_data.clear()
    assert len(queue_with_data) == 0


def test_queue_pop_task(queue_with_data):
    first_task = queue_with_data.pop_task()
    assert first_task.id == 1
    assert len(queue_with_data) == 2

    second_task = queue_with_data.pop_task()
    assert second_task.id == 2
    assert len(queue_with_data) == 1


def test_queue_pop_empty():
    q = TaskQueue()
    assert q.pop_task() is None