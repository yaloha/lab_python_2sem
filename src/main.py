import os.path as path
import random

import uvicorn
from fastapi import FastAPI, Depends
from constants import DEFAULT_EXTERNAL_API_URL
from protocols import TaskSource
from sources.api_source import APISource
from sources.file_source import FileSource
from sources.generator_source import GeneratorSource
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

def source_choice(file_name: str = "file.json", url: str = DEFAULT_EXTERNAL_API_URL, n: int = 5) -> TaskSource:
    curr_dir = path.dirname(path.abspath(__file__))
    file_path = path.join(curr_dir, file_name)
    return random.choice([
        FileSource(file_path),
        APISource(url),
        GeneratorSource(n)
    ])


@app.get("/tasks")
async def read_tasks(source: TaskSource = Depends(source_choice)):
    if not isinstance(source, TaskSource):
        raise TypeError("source does not follow TaskSource protocol")
    source_type = source.__class__.__name__

    logger.info(f"Fetching tasks using source: {source_type}")
    return await source.get_tasks()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)