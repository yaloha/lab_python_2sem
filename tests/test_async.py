import pytest
import asyncio
from src.models import Task
from src.handlers.handler_protocol import TaskHandler, EmailNotificationHandler
from src.handlers.task_executor import AsyncExecutor, TaskExecutionContext


@pytest.fixture
def sample_task():
    return Task(id=42, name="test_task", payload="meow", priority=2)


@pytest.mark.asyncio
async def test_task_execution_context_success(sample_task):
    async with TaskExecutionContext(sample_task) as ctx:
        assert sample_task.status.name == "IN_PROGRESS"

    assert sample_task.status.name == "DONE"


@pytest.mark.asyncio
async def test_task_execution_context_failure(sample_task):
    try:
        async with TaskExecutionContext(sample_task):
            raise RuntimeError
    except RuntimeError:
        pass

    assert sample_task.status.name == "CREATED"


def test_handler_protocol_conformance():
    handler = EmailNotificationHandler()
    assert isinstance(handler, TaskHandler)


@pytest.mark.asyncio
async def test_executor_processing(sample_task):
    executor = AsyncExecutor()

    class MockHandler:
        def __init__(self):
            self.called = False

        async def handle(self, task: Task):
            self.called = True

    mock_handler = MockHandler()

    sample_task.name = "event"
    executor.register_handler("event", mock_handler)

    await executor.enqueue_tasks([sample_task])
    await executor.start_processing(num_workers=3)

    await executor.stop_processing()

    assert mock_handler.called is True
    assert sample_task.status.name == "DONE"