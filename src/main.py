import os.path as path
import random
from typing import List
from src.handlers.task_executor import AsyncExecutor
from src.handlers.handler_protocol import EmailNotificationHandler, StatisticsHandler

import uvicorn
from fastapi import FastAPI, Depends, HTTPException

from src.pydantic_models import TaskSchema, TaskFilterResponse
from src.constants import DEFAULT_EXTERNAL_API_URL, DEFAULT_FILE_NAME, DEFAULT_RANDOM_TASKS_AMMOUNT
from src.models import Task
from src.protocols import TaskSource
from src.sources.api_source import APISource
from src.sources.file_source import FileSource
from src.sources.generator_source import GeneratorSource
from src.task_queue import TaskQueue
from src.models import TaskStatus
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

def source_choice(file_name: str = DEFAULT_FILE_NAME, url: str = DEFAULT_EXTERNAL_API_URL, n: int = DEFAULT_RANDOM_TASKS_AMMOUNT) -> TaskSource:
    """randomly chooses a task source from the 3 located in /sources directory,
    takes file_name, url and n -> settings for randomly chosen sources"""
    curr_dir = path.dirname(path.abspath(__file__))
    file_path = path.join(curr_dir, file_name)
    return random.choice([
        FileSource(file_path),
        APISource(url),
        GeneratorSource(n)
    ])


@app.get("/tasks", response_model=None)
async def read_tasks(source: TaskSource = Depends(source_choice)) -> List[TaskSchema]:
    """reads tasks from task source randomly chosen using source_choice and returns in to user (or any mistake should it arise)"""
    if not isinstance(source, TaskSource):
        logger.error(f"{type(source)} violates TaskSource protocol")
        raise HTTPException(
            status_code=500,
            detail="source protocol violation"
        )
    source_type = source.__class__.__name__

    logger.info(f"Fetching tasks using source: {source_type}")
    return await source.get_tasks()


@app.get("/tasks/p/{priority}", response_model=TaskFilterResponse)
async def process_tasks(priority: int, source: TaskSource = Depends(source_choice)):
    """demo endpoint that demonstrates filter_by_priority method"""
    queue = TaskQueue()
    await queue.load_from_source(source)
    all_tasks = [
        TaskSchema(id=t.id, name=t.name, payload=t.payload, priority=t.priority)
        for t in queue
    ]
    filtered_list = queue.filter_by_priority(priority)
    filtered_tasks = [
        TaskSchema(id=t.id, name=t.name, payload=t.payload, priority=t.priority)
        for t in filtered_list
    ]

    return {
        "description": f"filtration by priority >= {priority}",
        "total": len(queue),
        "original": all_tasks,
        "filtered": filtered_tasks
    }

@app.get("/tasks/s/{status}", response_model=TaskFilterResponse)
async def process_tasks(status: TaskStatus, source: TaskSource = Depends(source_choice)):
    """demo endpoint that demonstrates filter_by_status method"""
    queue = TaskQueue()
    await queue.load_from_source(source)
    all_tasks = [
        TaskSchema(id=t.id, name=t.name, payload=t.payload, priority=t.priority)
        for t in queue
    ]
    filtered_list = queue.filter_by_status(status)
    filtered_tasks = [
        TaskSchema(id=t.id, name=t.name, payload=t.payload, priority=t.priority)
        for t in filtered_list
    ]

    return {
        "filter_applied": status.value,
        "total": len(queue),
        "original": all_tasks,
        "filtered": filtered_tasks
    }

@app.post("/tasks/execute")
async def execute_tasks(workers: int = 2, source: TaskSource = Depends(source_choice)):
    """
    Endpoint starts task handling from the source
    """
    tasks_list = await source.get_tasks()
    if not tasks_list:
        return {"message": "Source returned empty task list"}

    executor = AsyncExecutor()

    executor.register_handler("notify", EmailNotificationHandler())
    executor.register_handler("calculate", StatisticsHandler())

    executor.register_handler("TASK_TITLE_1", EmailNotificationHandler())
    executor.register_handler("TASK_TITLE_2", StatisticsHandler())

    await executor.enqueue_tasks(tasks_list)
    await executor.start_processing(num_workers=workers)

    await executor.stop_processing()

    report = {
        "source_used": source.__class__.__name__,
        "total_received": len(tasks_list),
        "processed_states": [
            {"id": t.id, "name": t.name, "status": t.status.name} for t in tasks_list
        ]
    }
    return report

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="localhost", port=8000, reload=True)