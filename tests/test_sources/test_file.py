import pytest
import json
import tempfile
import os
from src.task_sources.file_source import FileSource
from src.task.task import Task

# JSON фикстуры
@pytest.fixture
def valid_json_file():
    data = [{"id": 1, "payload": "задача 1"}, {"id": 2, "payload": "задача 2"}]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)

@pytest.fixture
def invalid_json_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{это не json')
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)

# TXT фикстуры
@pytest.fixture
def valid_txt_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("1: задача 1\n2: задача 2")
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)

@pytest.fixture
def unsupported_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("1,задача 1")
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)

# Тесты JSON
def test_json_valid(valid_json_file):
    tasks = FileSource(valid_json_file).get_tasks()
    assert len(tasks) == 2
    assert tasks[0].id == 1

def test_json_invalid(invalid_json_file):
    with pytest.raises(Exception) as e:
        FileSource(invalid_json_file).get_tasks()
    assert "Ошибка при чтении JSON" in str(e.value)

def test_json_not_found():
    with pytest.raises(FileNotFoundError):
        FileSource("no.json").get_tasks()

# Тесты TXT
def test_txt_valid(valid_txt_file):
    tasks = FileSource(valid_txt_file).get_tasks()
    assert len(tasks) == 2
    assert tasks[0].id == "1"

def test_txt_not_found():
    with pytest.raises(FileNotFoundError):
        FileSource("no.txt").get_tasks()

# Тест неподдерживаемого формата
def test_unsupported_extension(unsupported_file):
    with pytest.raises(ValueError) as e:
        FileSource(unsupported_file).get_tasks()
    assert "не поддерживается" in str(e.value)