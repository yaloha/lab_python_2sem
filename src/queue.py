from typing import Iterable, Iterator
from src.models import Task, TaskStatus
from src.protocols import TaskSource

class TaskQueue:
    def __init__(self):
        self._tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    async def load_from_source(self, source: TaskSource) -> None:
        new_tasks = await source.get_tasks()
        for task_data in new_tasks:
            if isinstance(task_data, Task):
                self.add_task(task_data)


    def __iter__(self) -> Iterator[Task]:
        for task in self._tasks:
            yield task

    def __len__(self) -> int:
        return len(self._tasks)

    def filter_by_status(self, status: TaskStatus) -> Iterable[Task]:
        for task in self:
            if task.status == status:
                yield task

    def filter_by_priority(self, min_pr: int) -> Iterable[Task]:
        for task in self:
            if task.priority >= min_pr:
                yield task