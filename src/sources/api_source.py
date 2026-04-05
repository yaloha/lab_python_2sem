import httpx
from typing import List
from constants import DEFAULT_EXTERNAL_API_URL
from models import Task


class APISource:
    def __init__(self, url: str = DEFAULT_EXTERNAL_API_URL):
        self.url = url

    async def get_tasks(self) -> List[Task]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.url, timeout=5.0)

                response.raise_for_status()

                task_details = response.json()

                return [Task(**details) for details in task_details]

            except httpx.HTTPError as e:
                print(f"http error: {e}")
                return []
            except Exception as e:
                print(f"data parse error: {e}")
                return []