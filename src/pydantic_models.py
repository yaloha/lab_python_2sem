from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict


class TaskSchema(BaseModel):
    id: int
    name: str
    payload: str
    priority: int

class TaskStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class PydanticTask(BaseModel):
    """alternative implementation of Task class using pydantic. all validations and setters are implemented """
    id: int
    name: str = Field(min_length=3)
    payload: str = Field(min_length=1)
    priority: int = Field(default=1, ge=0, le=10)
    status: TaskStatus = Field(default=TaskStatus.CREATED)
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(frozen=True)

    @field_validator('name')
    @classmethod
    def name_not_blank(cls, s: str) -> str:
        """user validation (as __set__ in ValidatedString)"""
        if not s.strip():
            raise ValueError("name must be not blank")
        return s.strip()

    @property
    def is_urgent(self) -> bool:
        """calculated property works the same way"""
        return self.priority >= 5

    @property
    def summary(self) -> str:
        """as the non-data descriptor in Task"""
        return f"[{self.status.name}] #{self.id} - {self.name} (Priority: {self.priority})"

class TaskFilterResponse(BaseModel):
    filter_applied: Optional[str] = None
    description: Optional[str] = None
    total: int
    original: list[TaskSchema]
    filtered: list[TaskSchema]
