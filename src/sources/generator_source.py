import random
from src.models import Task, TaskStatus
import src.constants as constants

class GeneratorSource:
    def __init__(self, count: int = 5):
        """n param sets the ammount of tasks to generate, default is 5"""
        self.count = max(0, count)

    async def get_tasks(self) -> list[Task]:
        """returns a list of n-times generated tasks """
        tasks = []
        for _ in range(self.count):
            task = Task(
                id=random.randint(1, 9999999),
                name=random.choice(constants.TASK_TITLES),
                payload=random.choice(constants.TASK_PAYLOADS),
                priority=random.randint(1, 10)
            )
            task.status = random.choice(list(TaskStatus))
            tasks.append(task)
        return tasks