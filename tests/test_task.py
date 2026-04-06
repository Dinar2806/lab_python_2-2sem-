import pytest
from src.task.task import Task

def test_task_creation():
    task = Task(id=1, payload="тест")
    assert task.id == 1
    assert task.payload == "тест"

def test_task_with_different_types():
    task1 = Task(id=1, payload="строка")
    task2 = Task(id="uuid-123", payload=42)
    task3 = Task(id=3.14, payload={"key": "value"})
    
    assert isinstance(task1.id, int)
    assert isinstance(task2.id, str)
    assert isinstance(task3.id, float)
    assert task2.payload == 42
    assert task3.payload["key"] == "value"

def test_task_str_representation():
    task = Task(id=42, payload="данные")
    assert str(task) == "Task(id=42, payload=данные)"