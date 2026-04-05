TASK_TITLES = (
    "develop something",
    "make some tasks",
    "get started on a lab"
)

TASK_PAYLOADS = (
    "configure uv",
    "discuss sprint with a team",
    "stop doomscrolling"
)

API_MOCK_TASKS = [
    {"id": 1, "name": "pet a cat", "payload": "the tabby one!"},
    {"id": 2, "name": "buy a gift", "payload": "to my g(b)f"},
    {"id": 3, "name": "transfer to linux", "payload": "decide which one to use"},
]


DEFAULT_EXTERNAL_API_URL = "http://127.0.0.1:8001/api/v1/tasks"