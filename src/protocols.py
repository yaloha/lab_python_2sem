from typing import Protocol, runtime_checkable, List
from models import Task


@runtime_checkable
class TaskSource(Protocol):
    async def get_tasks(self) -> List[Task]:
        ...

