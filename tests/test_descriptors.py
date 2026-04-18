import pytest
from datetime import datetime
from src.models import Task, TaskStatus, TaskValidationError


def test_task_creation_valid():
    task = Task(id=1, name="meown", payload="bleh", priority=5)
    assert task.id == 1
    assert task.name == "meown"
    assert task.priority == 5
    assert task.status == TaskStatus.CREATED

def test_validated_string_min_len():
    with pytest.raises(TaskValidationError, match="length of 'name' must be >= 3"):
        Task(id=1, name="Ab", payload="Valid payload")

def test_validated_string_type():
    with pytest.raises(TaskValidationError, match="must be a string"):
        Task(id=1, name=123, payload="Valid")

def test_validated_priority():
    with pytest.raises(TaskValidationError, match="priority must lay in a range"):
        Task(id=1, name="Valid", payload="Valid", priority=11)

    with pytest.raises(TaskValidationError, match="priority must lay in a range"):
        Task(id=1, name="Valid", payload="Valid", priority=0)

def test_id_is_int_validation():
    with pytest.raises(TaskValidationError, match="id must be an integer"):
        
        t = Task(id=1, name="meow", payload="bleh", priority=1)
        t.task_id = "строка"

def test_status_setter_validation():
    task = Task(id=1, name="meow", payload="bleh")
    with pytest.raises(TaskValidationError, match="status must be of object TaskStatus."):
        task.status = "DONE"

def test_readonly_properties():
    task = Task(id=1, name="meow", payload="bleh")
    with pytest.raises(AttributeError):
        task.created_at = datetime.now()

    with pytest.raises(AttributeError):
        task.id = 100

def test_is_urgent():
    low_priority = Task(id=1, name="meow", payload="bleh", priority=4)
    high_priority = Task(id=2, name="meow", payload="bleh", priority=9)

    assert low_priority.is_urgent is False
    assert high_priority.is_urgent is True

def test_task_formatter_summary():
    task = Task(id=7, name="test", payload="bleh", priority=3)
    
    expected = '"CREATED" #7 - test (Priority: 3)'
    assert task.summary == expected