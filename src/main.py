import os.path as path
import random
from typing import List

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from src.constants import DEFAULT_EXTERNAL_API_URL, DEFAULT_FILE_NAME, DEFAULT_RANDOM_TASKS_AMMOUNT
from src.models import Task
from src.protocols import TaskSource
from src.sources.api_source import APISource
from src.sources.file_source import FileSource
from src.sources.generator_source import GeneratorSource
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


@app.get("/tasks")
async def read_tasks(source: TaskSource = Depends(source_choice)) -> List[Task]:
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)