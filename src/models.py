from dataclasses import dataclass
from typing import Any


@dataclass
class Task:
    id: int
    name: str
    payload: Any