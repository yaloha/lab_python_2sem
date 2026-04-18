import pytest
from datetime import datetime
from pydantic import ValidationError
from src.pydantic_models import PydanticTask, TaskStatus


def test_pydantic_task_valid():
    task = PydanticTask(id=1, name="valid name", payload="some payload", priority=5)
    assert task.id == 1
    assert task.name == "valid name"
    assert task.priority == 5
    assert task.status == TaskStatus.CREATED


def test_pydantic_name_min_len():
    with pytest.raises(ValidationError):
        PydanticTask(id=1, name="Ab", payload="buh")


def test_pydantic_name_blank():
    with pytest.raises(ValidationError, match=("name must be not blank")):
        PydanticTask(id=1, name="   ", payload="buh")


def test_pydantic_priority_range():
    with pytest.raises(ValidationError):
        PydanticTask(id=1, name="meow", payload="buh", priority=11)

    with pytest.raises(ValidationError):
        PydanticTask(id=1, name="meow", payload="buh", priority=-1)


def test_pydantic_types():
    with pytest.raises(ValidationError):
        PydanticTask(id="not_int", name="meow", payload="buh")


def test_pydantic_status_validation():
    with pytest.raises(ValidationError):
        PydanticTask(id=1, name="meow", payload="buh", status="INVALID_STATUS")


def test_pydantic_is_urgent():
    low = PydanticTask(id=1, name="mrow", payload="buh", priority=4)
    high = PydanticTask(id=2, name="mrow", payload="buh", priority=5)
    assert low.is_urgent is False
    assert high.is_urgent is True


def test_pydantic_summary():
    task = PydanticTask(id=10, name="coding", payload="buh", priority=7, status=TaskStatus.CREATED)
    expected = f"[CREATED] #10 - coding (Priority: 7)"
    assert task.summary == expected


def test_pydantic_readonly_behavior():
    task = PydanticTask(id=1, name="mrow", payload="buh")
    with pytest.raises(ValidationError):
        task.name = "sh"