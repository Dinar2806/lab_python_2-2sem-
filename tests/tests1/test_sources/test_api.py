import pytest
from src.task_sources.API_source import APISource
from src.task.task import Task

def test_api_source_default():
    source = APISource()
    tasks = source.get_tasks()
    
    assert len(tasks) == 3
    assert all(isinstance(t, Task) for t in tasks)
    assert tasks[0].id == "101"
    assert tasks[0].payload == "Задача из API #1"
    assert tasks[1].id == "102"
    assert tasks[2].id == "103"

def test_api_source_always_returns_same_data():
    source = APISource()
    tasks1 = source.get_tasks()
    tasks2 = source.get_tasks()
    
    assert len(tasks1) == len(tasks2)
    for t1, t2 in zip(tasks1, tasks2):
        assert t1.id == t2.id
        assert t1.payload == t2.payload

def test_api_source_data_structure():
    source = APISource()
    tasks = source.get_tasks()
    
    expected_payloads = [
        "Задача из API #1",
        "Задача из API #2",
        "Задача из API #3"
    ]
    
    for i, task in enumerate(tasks):
        assert task.payload == expected_payloads[i]

def test_api_source_multiple_calls_independent():
    source = APISource()
    tasks = source.get_tasks()
    
    # Изменение полученных задач не влияет на источник
    if tasks:
        tasks[0].id = "999"
    
    new_tasks = source.get_tasks()
    assert new_tasks[0].id == "101"