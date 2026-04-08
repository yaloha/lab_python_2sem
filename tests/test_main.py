import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.protocols import TaskSource

client = TestClient(app)

def test_read_tasks_endpoint():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_source_choice():
    from src.main import source_choice
    source = source_choice()
    assert isinstance(source, TaskSource)