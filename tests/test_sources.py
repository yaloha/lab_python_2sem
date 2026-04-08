import pytest
import json
from httpx import Response
from fastapi import HTTPException

from src.models import Task
from src.protocols import TaskSource
from src.sources.api_source import APISource
from src.sources.file_source import FileSource
from src.sources.generator_source import GeneratorSource


def test_protocol():
    assert isinstance(GeneratorSource(), TaskSource)
    assert isinstance(FileSource("test.json"), TaskSource)
    assert isinstance(APISource("http://meow.com"), TaskSource)

@pytest.mark.asyncio
async def test_generator_source():
    source = GeneratorSource(count=3)
    tasks = await source.get_tasks()
    assert len(tasks) == 3
    assert isinstance(tasks[0], Task)


@pytest.mark.asyncio
async def test_file_source(tmp_path):
    f = tmp_path / "tasks.json"
    mock_data = [{"id": 1, "name": "meow task!", "payload": "meow meow meow"}]
    f.write_text(json.dumps(mock_data))

    source = FileSource(str(f))
    tasks = await source.get_tasks()
    assert tasks[0].id == 1



@pytest.mark.asyncio
async def test_api_source(respx_mock):
    url = "http://meow-api.com/tasks"

    respx_mock.get(url).mock(return_value=Response(200, json=[
        {"id": 7, "name": "meow task", "payload": "from api"}
    ]))

    source = APISource(url)
    tasks = await source.get_tasks()

    assert tasks[0].id == 7
    assert respx_mock.get(url).called


@pytest.mark.asyncio
async def test_api_source_error(respx_mock):
    url = "http://meow-api.com/tasks"
    respx_mock.get(url).mock(return_value=Response(500))

    source = APISource(url)
    with pytest.raises(HTTPException) as exc:
        await source.get_tasks()

    assert exc.value.status_code == 502