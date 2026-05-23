import asyncio
import logging
from typing import Protocol, runtime_checkable
from src.models import Task

logger = logging.getLogger(__name__)

@runtime_checkable
class TaskHandler(Protocol):
    """data model setting a protocol to adhere to for task handlers"""
    async def handle(self, task: Task) -> None:
        ...

class EmailNotificationHandler:
    """handler for sending notifications from email"""
    async def handle(self, task: Task) -> None:
        logger.info(f"[EmailHandler] sending email for #{task.id}")
        await asyncio.sleep(1.5)
        logger.info(f"[EmailHandler] successful email send for #{task.id}. data: {task.payload}")


class StatisticsHandler:
    """handler for calculating statistics"""
    async def handle(self, task: Task) -> None:
        logger.info(f"[StatsHandler] calculating stats for #{task.id}")
        await asyncio.sleep(0.5)
        if "error" in task.payload.lower():
            raise ValueError("error happened while calculating stats")
        logger.info(f"[StatsHandler] stats are refreshed for #{task.id}")