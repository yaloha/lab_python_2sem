from datetime import datetime
from enum import Enum
from typing import Any

class TaskValidationError(Exception):
    """error class for task validation"""
    pass

class ValidatedString:
    """checks that the string is lengthier than min_len"""
    def __init__(self, min_len: int = 1):
        self.min_length = min_len
        self.name = None

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TaskValidationError(f"attribute '{self.name.lstrip('_')}' must be a string")
        if len(value.strip()) < self.min_length:
            raise TaskValidationError(f"length of '{self.name.lstrip('_')}' must be >= {self.min_length}.")
        setattr(instance, self.name, value.strip())

class ValidateIsInt:
    "validates that attribute is an int"
    def __init__(self):
        self.name = None

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TaskValidationError(f"{self.name.lstrip('_')} must be an integer")
        setattr(instance, self.name, value)

class ValidatedPriority:
    """checks that priority lies between min_val and max_val"""
    def __init__(self, min_val: int = 1, max_val: int = 10):
        self.min_val = min_val
        self.max_val = max_val
        self.name = None

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TaskValidationError("priority must be an integer")
        if not (self.min_val <= value <= self.max_val):
            raise TaskValidationError(f"priority must lay in a range from {self.min_val} to {self.max_val}.")
        setattr(instance, self.name, value)

class TaskFormatter:
    """non-data descriptor for formatted task output"""
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return f'"{instance.status.name}" #{instance.id} - {instance.name} (Priority: {instance.priority})'


class TaskStatus(Enum):
    "enum for task statuses"
    CREATED = "created"
    IN_PROGRESS = "in progress"
    DONE = "done"


class Task:
    """task model with validation using descriptors"""
    name = ValidatedString(min_len=3)
    payload = ValidatedString(min_len=1)
    priority = ValidatedPriority(min_val=1, max_val=10)
    task_id = ValidateIsInt()

    summary = TaskFormatter()

    def __init__(self, id: int, name: str, payload: Any, priority: int = 1):
        self.task_id = id
        self.name = name
        self.payload = str(payload)
        self.priority = priority

        self._status = TaskStatus.CREATED
        self._created_at = datetime.now()

    @property
    def id(self) -> int:
        """returns protected id"""
        return self._task_id

    @property
    def created_at(self) -> datetime:
        """returns protected created_at"""
        return self._created_at

    @property
    def status(self) -> TaskStatus:
        """returns protected status"""
        return self._status

    @status.setter
    def status(self, new_status: TaskStatus):
        """no string that isn't TaskStatus can be a status"""
        if not isinstance(new_status, TaskStatus):
            raise TaskValidationError("status must be of object TaskStatus.")
        self._status = new_status

    @property
    def is_urgent(self) -> bool:
        """task with a priority >= 5 is considered urgent"""
        return self.priority >= 5

    def __repr__(self):
        return f"Task(id={self.id}, name='{self.name}', status='{self.status.value}')"