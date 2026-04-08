import random
from src.models import Task
import src.constants as constants

class GeneratorSource:
    def __init__(self, count: int = 5):
        """n param sets the ammount of tasks to generate, default is 5"""
        self.count = max(0, count)

    async def get_tasks(self) -> list[Task]:
        """returns a list of n-times generated tasks """
        return [
            Task(
                id = random.randint(1, 9999999),
                name = random.choice(constants.TASK_TITLES),
                payload = random.choice(constants.TASK_PAYLOADS)
            )
            for _ in range(self.count)
        ]