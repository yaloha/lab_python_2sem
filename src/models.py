from dataclasses import dataclass


@dataclass
class Task:
    id: int
    name: str
    payload: dict