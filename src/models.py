from dataclasses import dataclass
from typing import Any


@dataclass
class Task:
    """data model representing a task"""
    id: int
    name: str
    payload: Any