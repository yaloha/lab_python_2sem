import asyncio
import logging
import time
from typing import Dict, Type
from fastapi import HTTPException

from src.models import Task, TaskStatus
from src.handlers.handler_protocol import TaskHandler

logger = logging.getLogger(__name__)


class TaskExecutionContext:
    """
    async context for managing tasks TTL
    """

    def __init__(self, task: Task):
        self.task = task
        self.start_time: float = 0.0

    async def __aenter__(self):
        self.start_time = time.monotonic()
        self.task.status = TaskStatus.IN_PROGRESS
        logger.info(f"Start of task managing #{self.task.id} [{self.task.name}]")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        duration = time.monotonic() - self.start_time
        if exc_type:
            logger.error(
                f"Error executing task #{self.task.id}: {exc_val}. "
                f"Status is set to CREATED. Execution time: {duration:.2f}s"
            )
            self.task.status = TaskStatus.CREATED
            return True

        self.task.status = TaskStatus.DONE
        logger.info(f"Successful task execution #{self.task.id}. Execution time: {duration:.2f}s")
        return False


class AsyncExecutor:
    """
    async executor handling the tasks to handlers
    """

    def __init__(self):
        self._handlers: Dict[str, TaskHandler] = {}
        self._queue: asyncio.Queue[Task] = asyncio.Queue()
        self._workers_tasks = []

    def register_handler(self, task_name: str, handler: TaskHandler) -> None:
        """register handler for some task type"""
        if not isinstance(handler, TaskHandler):
            raise TypeError(f"Handler {handler.__class__.__name__} must adhere to TaskHandler protocol")
        self._handlers[task_name] = handler
        logger.info(f"Registered handler {handler.__class__.__name__} for tasks of '{task_name}'")

    async def enqueue_tasks(self, tasks: list[Task]) -> None:
        """Queue tasks butch"""
        for task in tasks:
            await self._queue.put(task)
            logger.info(f"Task #{task.id} has been added to execution queue")

    async def _worker(self, worker_id: int) -> None:
        """Async worker handling the queue"""
        logger.info(f"Async worker #{worker_id} has started.")
        while True:
            task = await self._queue.get()
            try:
                handler = self._handlers.get(task.name)
                if not handler:
                    logger.warning(f"No handler for such task type '{task.name}' Task id: {task.id}")
                    continue

                async with TaskExecutionContext(task):
                    await handler.handle(task)

            finally:
                self._queue.task_done()

    async def start_processing(self, num_workers: int = 3) -> None:
        """initiate a pool of async workers"""
        self._workers_tasks = [
            asyncio.create_task(self._worker(i)) for i in range(num_workers)
        ]

    async def stop_processing(self) -> None:
        """close async workers pool"""
        await self._queue.join()
        for worker in self._workers_tasks:
            worker.cancel()
        await asyncio.gather(*self._workers_tasks, return_exceptions=True)
        self._workers_tasks.clear()
        logger.info("async pool has been closed")