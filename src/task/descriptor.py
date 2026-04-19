from typing import Any, Type, Optional, Union
from enum import Enum


# Специализированные исключения
class TaskValidationError(Exception):
    """Базовое исключение для ошибок валидации задачи."""
    pass

class InvalidPriorityError(TaskValidationError):
    """Выбрасывается, если приоритет выходит за допустимые границы."""
    pass

class InvalidStatusError(TaskValidationError):
    """Выбрасывается, если статус не является допустимым значением TaskStatus."""
    pass

class InvalidIdError(TaskValidationError):
    """Выбрасывается, если ID некорректен."""
    pass

class InvalidPayloadError(TaskValidationError):
    """Выбрасывается, если тело задачи некорректно."""
    pass


# Дескрипторы
class IDDescriptor:
    def __init__(self, min_val = 0):
        self.min_val = min_val
        
    def __set_name__(self, owner, name):
        self.private_name = "_" + name
        self.public_name = name
        
    def __get__(self, obj: Any, objtype: Type):
        if obj is None:
            return self
        
        return getattr(obj, self.private_name, self.min_val)
    
    def __set__(self, obj: Any, value: Any):
        normalized_id = str(value)
        
        if int(value) < self.min_val:
            raise ValueError(f"Минимальное возможное ID - {self.min_val}")
        
        setattr(obj, self.private_name, normalized_id)
        
    def __delete__(self, obj: Any) -> None:
        raise AttributeError("Невозможно удалить атрибут id")
    

class PriorityDescriptor:
    def __init__(self, highest_prior = 1, lowest_prior = 10):
        self.lowest_prior = lowest_prior
        self.highest_prior = highest_prior
        
        
    def __set_name__(self, owner, name):
        self.private_name = "_" + name
        self.public_name = name
        
    def __get__(self, obj: Any, objtype: Type):
        if obj is None:
            return self
        
        return getattr(obj, self.private_name, self.highest_prior)
    
    def __set__(self, obj: Any, value: Union[int, str]) -> None:
        
        if not isinstance(value, int):
            raise InvalidPriorityError(f"Приоритет должен быть целым числом, получено: {type(value)}")
        
        if not (self.highest_prior <= value <= self.lowest_prior):
            raise InvalidPriorityError(
                f"Приоритет должен быть в диапазоне [{self.highest_prior}, {self.lowest_prior}], получено: {value}"
            )
        
        setattr(obj, self.private_name, value)
        
    def __delete__(self, obj: Any) -> None:
        raise AttributeError("Невозможно удалить атрибут priority")
    
    

class StatusDescriptor:
    def __init__(self, expected_enum_type: Type[Enum], default_status: Enum = None):
        self.expected_enum_type = expected_enum_type
        self.default_status = default_status
    
    def __set_name__(self, owner: Type, name: str) -> None:
        self.public_name = name
        self.private_name = "_" + name
        
    def __get__(self, obj: Any, objtype: Type = None) -> Enum:
        if obj is None:
            return self
        return getattr(obj, self.private_name)
    
    def __set__(self, obj: Any, value: Any) -> None:
        # if isinstance(value, str):
        #     try:
        #         normalized_status = self.expected_enum_type(value)
        #     except:
        #         raise ValueError(f"Ошибка - не найден элемент {value} в {self.expected_enum_type}")
        # else:
        #     normalized_status = value
            
        if not isinstance(value, self.expected_enum_type):
             raise InvalidStatusError(f"Статус должен быть экземпляром Enum, получено: {type(value)}")
        
        setattr(obj, self.private_name, value)

    def __delete__(self, obj: Any) -> None:
        raise AttributeError(f"Невозможно удалить атрибут '{self.public_name}'")
    
class PayloadDescriptor:
    def __init__(self, default_value: str):
        self.default_value = default_value
        
    def __set_name__(self, owner: Type, name: str):
        self.public_name = name
        self.private_name = "_" + name
        
    def __get__(self, obj: Any, objtype: Type = None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, self.default_value)
    
    def __set__(self, obj: Any, value: Any):
        if not value:
            raise InvalidPayloadError("Тело задачи не может быть пустым")
        
        
        setattr(obj, self.private_name, value)
        
    def __delete__(self, obj: Any) -> None:
        raise AttributeError(f"Невозможно удалить атрибут '{self.public_name}'")
    

        
        
        
        
    
        
        
    