import pytest
from enum import Enum

from src.task.descriptor import (
    PriorityDescriptor, 
    StatusDescriptor, 
    PayloadDescriptor, 
    IDDescriptor,
    InvalidPriorityError, 
    InvalidStatusError, 
    InvalidPayloadError,
    TaskValidationError
)
from src.task.task import Task, TaskStatus

# фикстуры и вспомогательные классы

class MockEnum(Enum):
    A = "a"
    B = "b"

@pytest.fixture
def valid_task_data():
    return {
        "id": 1,
        "payload": "Test payload",
        "priority": 5,
        "status": TaskStatus.TODO
    }

# Тесты для PriorityDescriptor

class TestPriorityDescriptor:
    def test_valid_priority(self):
        """Проверка установки корректного приоритета"""
        desc = PriorityDescriptor()
        obj = type('Obj', (), {})() # Создаем пустой объект для теста
        desc.__set_name__(type(obj), 'priority')

        
        desc.__set__(obj, 5)
        assert desc.__get__(obj, Task) == 5

    def test_invalid_priority_type(self):
        """Проверка ошибки при передаче строки вместо int"""
        desc = PriorityDescriptor()
        obj = type('Obj', (), {})()
        desc.__set_name__(type(obj), 'priority')
        
        with pytest.raises(InvalidPriorityError):
            desc.__set__(obj, "high")

    def test_priority_out_of_range_low(self):
        """Проверка ошибки при приоритете меньше минимума"""
        desc = PriorityDescriptor()
        obj = type('Obj', (), {})()
        desc.__set_name__(type(obj), 'priority')
        
        with pytest.raises(InvalidPriorityError):
            desc.__set__(obj, 0)

    def test_priority_out_of_range_high(self):
        """Проверка ошибки при приоритете больше максимума"""
        desc = PriorityDescriptor()
        obj = type('Obj', (), {})()
        desc.__set_name__(type(obj), 'priority')
        
        with pytest.raises(InvalidPriorityError):
            desc.__set__(obj, 11)

    def test_default_priority(self):
        """Проверка значения по умолчанию, если атрибут не установлен"""
        desc = PriorityDescriptor()
        obj = type('Obj', (), {})()
        desc.__set_name__(type(obj), 'priority')
        
        assert desc.__get__(obj, Task) == 1 

# Тесты для StatusDescriptor

class TestStatusDescriptor:
    def test_valid_status(self):
        desc = StatusDescriptor(TaskStatus)
        obj = type('Obj', (), {})()
        desc.__set_name__(type(obj), 'status')
        
        desc.__set__(obj, TaskStatus.IN_PROGRESS)
        assert desc.__get__(obj) == TaskStatus.IN_PROGRESS

    def test_invalid_status_type(self):
        """Ошибка при передаче строки вместо Enum"""
        desc = StatusDescriptor(TaskStatus)
        obj = type('Obj', (), {})()
        desc.__set_name__(type(obj), 'status')
        
        with pytest.raises(InvalidStatusError):
            desc.__set__(obj, "todo") # Строка, а не Enum

    def test_invalid_enum_class(self):
        """Ошибка при передаче Enum другого типа"""
        desc = StatusDescriptor(TaskStatus)
        obj = type('Obj', (), {})()
        desc.__set_name__(type(obj), 'status')
        
        with pytest.raises(InvalidStatusError):
            desc.__set__(obj, MockEnum.A)

# Тесты для PayloadDescriptor

class TestPayloadDescriptor:
    def test_valid_payload(self):
        desc = PayloadDescriptor(default_value="default")
        obj = type('Obj', (), {})()
        desc.__set_name__(type(obj), 'payload')
        
        desc.__set__(obj, "Hello World")
        assert desc.__get__(obj) == "Hello World"

    def test_empty_payload_error(self):
        """Ошибка при пустой строке"""
        desc = PayloadDescriptor(default_value="default")
        obj = type('Obj', (), {})()
        desc.__set_name__(type(obj), 'payload')
        
        with pytest.raises(InvalidPayloadError):
            desc.__set__(obj, "")

    def test_none_payload_error(self):
        """Ошибка при None"""
        desc = PayloadDescriptor(default_value="default")
        obj = type('Obj', (), {})()
        desc.__set_name__(type(obj), 'payload')
        
        with pytest.raises(InvalidPayloadError):
            desc.__set__(obj, None)



# Интеграционные тесты класса Task

class TestTaskModel:
    def test_create_valid_task(self, valid_task_data):
        """Создание корректной задачи"""
        task = Task(**valid_task_data)
        assert task.id == "1"
        assert task.payload == "Test payload"
        assert task.priority == 5
        assert task.status == TaskStatus.TODO

    def test_task_ready_to_perform(self, valid_task_data):
        """Проверка вычисляемого свойства ready_to_perform"""
        task = Task(**valid_task_data)
        assert task.ready_to_perform is True
        
        task.status = TaskStatus.DONE
        assert task.ready_to_perform is False

    def test_task_invalid_priority_via_constructor(self):
        """Ошибка при создании задачи с неверным приоритетом"""
        with pytest.raises(InvalidPriorityError):
            Task(id=1, payload="Test", priority=100)

    def test_task_invalid_status_via_assignment(self, valid_task_data):
        """Ошибка при присвоении неверного статуса существующей задаче"""
        task = Task(**valid_task_data)
        with pytest.raises(InvalidStatusError):
            task.status = "invalid_string"

    def test_task_payload_validation(self):
        """Проверка валидации payload при создании"""
        with pytest.raises(InvalidPayloadError):
            Task(id=1, payload="", priority=5, status=TaskStatus.TODO)

    def test_task_id_validation(self):
        """Проверка валидации ID (если используется IDDescriptor или логика в init)"""
        
        pass