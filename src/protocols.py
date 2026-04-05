from typing import Protocol, runtime_checkable, List
from models import Task


@runtime_checkable
class TaskSource(Protocol):
    """data model setting a protocol to adhere to for task sources"""
    async def get_tasks(self) -> List[Task]:
        ...

