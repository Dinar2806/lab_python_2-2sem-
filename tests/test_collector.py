import pytest
from src.task.task import Task
from src.task_sources.protocol import TaskSourceProtocol
from src.task_sources.API_source import APISource
from src.task_sources.file_source import FileSource
from src.task_sources.generator_source import GeneratorSource
from src.task_collector.collector import TaskCollector, quick_collect

class MockSource:
    def __init__(self, tasks):
        self.tasks = tasks
    
    def get_tasks(self):
        return self.tasks

class InvalidSource:
    pass

def test_collector_initial_state():
    collector = TaskCollector()
    assert collector.get_all_tasks() == []

def test_collector_accepts_valid_source():
    source = MockSource([Task(id=1, payload="тест")])
    collector = TaskCollector()
    
    tasks = collector.collect(source)
    assert len(tasks) == 1
    assert tasks[0].id == 1

def test_collector_rejects_invalid_source():
    collector = TaskCollector()
    invalid = InvalidSource()
    
    with pytest.raises(TypeError) as excinfo:
        collector.collect(invalid)
    assert "не соответствует контракту" in str(excinfo.value)

def test_collector_handles_id_conflicts():
    collector = TaskCollector()
    
    source1 = MockSource([
        Task(id=1, payload="первая"),
        Task(id=2, payload="вторая")
    ])
    
    source2 = MockSource([
        Task(id=1, payload="конфликт"),
        Task(id=3, payload="третья")
    ])
    
    collector.collect(source1)
    collector.collect(source2)
    
    all_tasks = collector.get_all_tasks()
    assert len(all_tasks) == 4
    
    ids = [t.id for t in all_tasks]
    assert 1 in ids
    assert 2 in ids
    assert 3 in ids
    

def test_collector_preserves_payload_on_conflict():
    collector = TaskCollector()
    
    source1 = MockSource([Task(id=1, payload="оригинал")])
    source2 = MockSource([Task(id=1, payload="дубликат")])
    
    collector.collect(source1)
    collector.collect(source2)
    
    tasks = collector.get_all_tasks()
    assert len(tasks) == 2
    
    # Находим задачу с конфликтным payload
    conflict_task = next(t for t in tasks if t.payload == "дубликат")
    assert conflict_task.id != 1

def test_collector_multiple_sources_no_conflicts():
    collector = TaskCollector()
    
    sources = [
        MockSource([Task(id=i, payload=f"src1_{i}") for i in range(3)]),
        MockSource([Task(id=i+10, payload=f"src2_{i}") for i in range(3)]),
        MockSource([Task(id=i+20, payload=f"src3_{i}") for i in range(3)])
    ]
    
    for source in sources:
        collector.collect(source)
    
    all_tasks = collector.get_all_tasks()
    assert len(all_tasks) == 9
    
    ids = [t.id for t in all_tasks]
    assert sorted(ids) == list(range(3)) + list(range(10, 13)) + list(range(20, 23))

def test_collector_quick_collect_function():
    sources = [
        MockSource([Task(id=1, payload="a")]),
        MockSource([Task(id=2, payload="b")])
    ]
    
    tasks = quick_collect(sources)
    assert len(tasks) == 2
    assert tasks[0].id == 1
    assert tasks[1].id == 2

def test_collector_empty_source():
    collector = TaskCollector()
    source = MockSource([])
    
    tasks = collector.collect(source)
    assert tasks == []
    assert collector.get_all_tasks() == []

def test_collector_id_generation_sequential():
    collector = TaskCollector()
    
    source1 = MockSource([Task(id=5, payload="a")])
    source2 = MockSource([Task(id=5, payload="b"), Task(id=5, payload="c")])
    
    collector.collect(source1)
    collector.collect(source2)
    
    tasks = collector.get_all_tasks()
    ids = [t.id for t in tasks]
    
    assert 5 in ids
    # Должны быть сгенерированы новые уникальные ID
    assert len(set(ids)) == 3
    assert all(isinstance(id, int) for id in ids)

