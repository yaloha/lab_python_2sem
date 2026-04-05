import random
from models import Task
import constants as constants

class GeneratorSource:
    def __init__(self, count: int = 15):
        self.count = max(0, count)

    async def get_tasks(self) -> list[Task]:
        return [
            Task(
                id = random.randint(1, 9999999),
                name = random.choice(constants.TASK_TITLES),
                payload = random.choice(constants.TASK_PAYLOADS)
            )
            for _ in range(self.count)
        ]