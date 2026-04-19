import pytest
from src.task.task import Task, TaskStatus

def test_task_creation():
    task = Task(id=1, payload="тест", priority=4, status=TaskStatus.TODO)
    assert task.id == "1"
    assert task.payload == "тест"
    assert task.priority == 4
    assert task.status == TaskStatus.TODO

def test_task_with_different_types():
    task1 = Task(id=1, payload="строка", priority=4, status=TaskStatus.TODO)
    task2 = Task(id="123", payload=42, priority=8, status=TaskStatus.TODO)
    task3 = Task(id=3.14, payload={"key": "value"}, priority=5, status=TaskStatus.TODO)
    
    assert isinstance(task1.id, str)
    assert isinstance(task2.id, str)
    assert isinstance(task3.id, str)
    
    assert task1.payload == "строка"
    assert task2.payload == 42
    assert task3.payload["key"] == "value"
    
    assert task1.priority == 4
    assert task2.priority == 8
    assert task3.priority == 5
        
    assert task1.status == TaskStatus.TODO
    assert task2.status == TaskStatus.TODO
    assert task3.status == TaskStatus.TODO
    
    

def test_task_str_representation():
    task = Task(id=42, payload="данные", priority=4, status=TaskStatus.TODO)
    assert str(task) == "Task(id=42, payload=данные)"