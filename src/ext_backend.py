from typing import List

from fastapi import FastAPI
from constants import API_MOCK_TASKS
from models import Task

app = FastAPI()

mock_tasks = API_MOCK_TASKS
@app.get("/api/v1/tasks")
async def get_external_tasks() -> List[Task]:
    """mock api to return a list of tasks specified in constants file"""
    return mock_tasks

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)