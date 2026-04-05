import json
from os.path import exists as path_exists
from typing import List

from fastapi import HTTPException

from models import Task
import logging


logger = logging.getLogger(__name__)

class FileSource:
    def __init__(self, json_file: str):
        """initializes file source, self.file_path is set using json_file param,
        it is responsible for file name, it should be of json format"""
        self.file_path = json_file

    async def get_tasks(self) -> List[Task]:
        """returns a list of all tasks from file located at self.file_path, file should be of json format"""
        if not path_exists(self.file_path):
            raise HTTPException(status_code=404, detail=f"file {self.file_path} not found")

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                task_details = json.load(file)
            return [Task(**details) for details in task_details]

        except Exception as e:
            logger.error(f"unexpected error {self.file_path}: {e}")
            raise HTTPException(status_code=500, detail="internal server error")