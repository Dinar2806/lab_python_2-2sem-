import pytest
from src.task_sources.generator_source import GeneratorSource
from src.task.task import Task

def test_generator_default():
    source = GeneratorSource()
    tasks = source.get_tasks()
    
    assert len(tasks) == 5
    assert all(isinstance(t, Task) for t in tasks)
    assert tasks[0].id == "0"
    assert tasks[4].id == "4"

def test_generator_with_custom_count():
    source = GeneratorSource(count=10)
    tasks = source.get_tasks()
    
    assert len(tasks) == 10
    assert tasks[0].id == "0"
    assert tasks[9].id == "9"

def test_generator_with_id_start():
    source = GeneratorSource(count=3, id_start=100)
    tasks = source.get_tasks()
    
    assert len(tasks) == 3
    assert tasks[0].id == "100"
    assert tasks[1].id == "101"
    assert tasks[2].id == "102"

def test_generator_payload_content():
    source = GeneratorSource(count=2)
    tasks = source.get_tasks()
    
    # В классе нет текста "Сгенерированная задача", там фразы вроде "Убрать мусор..."
    # Проверяем просто, что payload — это строка и она не пустая
    assert isinstance(tasks[0].payload, str)
    assert len(tasks[0].payload) > 0

def test_generator_zero_count():
    # Ошибка выбрасывается в __init__, поэтому оборачиваем создание объекта
    with pytest.raises(ValueError, match="положительным числом"):
        GeneratorSource(count=0)

def test_generator_negative_count():
    # Аналогично, ошибка возникнет сразу при создании
    with pytest.raises(ValueError, match="положительным числом"):
        GeneratorSource(count=-5)

def test_generator_consistency():
    # Т.к. используется random, объекты будут разными. 
    # Проверяем только ID, они должны совпадать.
    source1 = GeneratorSource(count=3, id_start=10)
    source2 = GeneratorSource(count=3, id_start=10)
    
    tasks1 = source1.get_tasks()
    tasks2 = source2.get_tasks()
    
    for t1, t2 in zip(tasks1, tasks2):
        assert t1.id == t2.id
        # assert t1.payload == t2.payload  <-- Это удаляем, random выдаст разное


