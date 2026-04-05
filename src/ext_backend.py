from fastapi import FastAPI
from constants import API_MOCK_TASKS
app = FastAPI()

mock_tasks = API_MOCK_TASKS
@app.get("/api/v1/tasks")
async def get_external_tasks():
    return mock_tasks

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)