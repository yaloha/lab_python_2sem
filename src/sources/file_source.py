import json
from os.path import exists as path_exists
from typing import List

from fastapi import HTTPException

from models import Task
import logging


logger = logging.getLogger(__name__)

class FileSource:
    def __init__(self, parsing_file: str):
        self.file_path = parsing_file

    async def get_tasks(self) -> List[Task]:
        if not path_exists(self.file_path):
            raise HTTPException(status_code=404, detail=f"file {self.file_path} not found")

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                task_details = json.load(file)
            return [Task(**details) for details in task_details]

        except Exception as e:
            logger.error(f"unexpected error {self.file_path}: {e}")
            raise HTTPException(status_code=500, detail="internal server error")