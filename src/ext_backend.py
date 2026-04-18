from typing import List

from fastapi import FastAPI
from src.constants import API_MOCK_TASKS
from src.pydantic_models import TaskSchema

app = FastAPI()

mock_tasks = API_MOCK_TASKS
@app.get("/api/v1/tasks", response_model=List[TaskSchema])
async def get_external_tasks() -> List[TaskSchema]:
    """mock api to return a list of tasks specified in constants file"""
    return mock_tasks

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)