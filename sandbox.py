import sys

# Перенастраиваем стандартный вывод на UTF-8
sys.stdout.reconfigure(encoding='utf-8')




class AgeDescriptor:
    def __init__(self, name):
        self.name = '_' + name  # Скрытое имя атрибута

    def __get__(self, instance, owner):
        print(f"Получение {self.name}")
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        print(f"Установка {self.name} = {value}")
        if not isinstance(value, int) or value < 0 or value > 120:
            raise ValueError("Возраст должен быть числом от 0 до 120")
        setattr(instance, self.name, value)

class Person:
    # Использование дескриптора
    age = AgeDescriptor("age")

    def __init__(self, name, age):
        self.name = name
        self.age = age  # Вызовется __set__

# Использование

p = Person("Ivan", 25)
print(p._age)
