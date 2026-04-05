import httpx
from typing import List

from fastapi import HTTPException
import logging
from constants import DEFAULT_EXTERNAL_API_URL
from models import Task


logger = logging.getLogger(__name__)


class APISource:
    def __init__(self, url: str = DEFAULT_EXTERNAL_API_URL):
        "initializes API source with URL, at this URL GET endpoint that returns List[Task] should be located"
        self.url = url

    async def get_tasks(self) -> List[Task]:
        """returns a list of all tasks from remote API that has a GET endpoint located at self.url"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.url, timeout=5.0)

                response.raise_for_status()

                task_details = response.json()

                return [Task(**details) for details in task_details]

            except httpx.HTTPError as e:
                logger.error(f"External API communication error: {e}")
                raise HTTPException(status_code=502, detail="external API communication error")
            except Exception as e:
                logger.error(f"unexpected error in external API: {e}")
                raise HTTPException(status_code=500, detail="internal error while fetching external tasks")