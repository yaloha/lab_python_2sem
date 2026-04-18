from typing import Iterable, Iterator
from src.models import Task, TaskStatus
from src.protocols import TaskSource

class TaskQueue:
    """container for Task objects"""
    def __init__(self):
        """initializes an empty task queue"""
        self._tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """appends a single task to the end of the queue"""
        self._tasks.append(task)

    async def load_from_source(self, source: TaskSource) -> None:
        """fetch tasks from external source"""
        new_tasks = await source.get_tasks()
        for task_data in new_tasks:
            if isinstance(task_data, Task):
                self.add_task(task_data)

    def __iter__(self) -> Iterator[Task]:
        """yields tasks one by one from the queue"""
        for task in self._tasks:
            yield task

    def __len__(self) -> int:
        """returns the total number of tasks in the queue"""
        return len(self._tasks)

    def filter_by_status(self, status: TaskStatus) -> Iterable[Task]:
        """generate tasks that match a status set as argument"""
        for task in self:
            if task.status == status:
                yield task

    def filter_by_priority(self, min_pr: int) -> Iterable[Task]:
        """generate tasks with priority >= than the min_pr argument"""
        for task in self:
            if task.priority >= min_pr:
                yield task

    def __getitem__(self, item: int | slice) -> Task | list[Task]:
        """access tasks from queue using indexing or slicing"""
        return self._tasks[item]

    def __contains__(self, task: Task | int) -> bool:
        """check if task exists in the queue"""
        if isinstance(task, int):
            return any(t.id == task for t in self._tasks)
        return any(t.id == task.id for t in self._tasks)

    def clear(self) -> None:
        """remove all tasks from the queue."""
        self._tasks.clear()

    def pop_task(self) -> Task:
        """pop task from the queue (FIFO)"""
        if not self._tasks:
            return None
        return self._tasks.pop(0)