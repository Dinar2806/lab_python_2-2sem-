"""
Модуль содержит коллектор задач из разных источников
"""

from typing import List, Dict, Set, Optional, Union
from src.task.task import Task
from src.task_sources.protocol import TaskSourceProtocol


class TaskCollector:
    """
    Коллектор задач из различных источников.
    
    Собирает задачи из источников, соответствующих протоколу TaskSourceProtocol,
    и управляет уникальностью ID задач.
    
    Attributes:
        _all_tasks: Список всех собранных задач
        _used_ids: Множество использованных ID для отслеживания дубликатов
        _next_id: Счетчик для генерации новых ID при конфликтах
    """
    
    def __init__(self):
        """Инициализирует пустой коллектор."""
        self._all_tasks: List[Task] = []
        self._used_ids: Set[Union[int, str]] = set()
        self._next_id: int = 1
        self._conflicts_count: int = 0
    
    def collect(self, source: TaskSourceProtocol, fix_conflicts: bool = True) -> List[Task]:
        """
        Собирает задачи из указанного источника.
        
        Args:
            source: Источник задач (должен соответствовать протоколу)
            fix_conflicts: Исправлять ли конфликты ID (если False - просто предупреждать)
            
        Returns:
            List[Task]: Список задач, полученных из источника
            
        Raises:
            TypeError: Если источник не соответствует протоколу
            Exception: Любые исключения от источника пробрасываются дальше
        """
        #ПРОВЕРКА КОНТРАКТА!
        if not isinstance(source, TaskSourceProtocol):
            raise TypeError(
                f"Объект {type(source).__name__} не соответствует контракту ")
        
        #Получаем задачи из источника
        print(f"Сбор задач из {type(source).__name__}...")
        new_tasks = source.get_tasks()
        print(f"  Получено {len(new_tasks)} задач")
        
        #Обработка конфликтов
        if fix_conflicts:
            resolved_tasks = self._resolve_id_conflicts(new_tasks)
        else:
            resolved_tasks = new_tasks
            self._check_conflicts(new_tasks)
        
        #Добавляем в общее хранилище
        for task in resolved_tasks:
            self._all_tasks.append(task)
            self._used_ids.add(task.id)
        
        return resolved_tasks
    
    def collect_from_sources(self, sources: List[TaskSourceProtocol]) -> Dict[str, List[Task]]:
        """
        Собирает задачи из нескольких источников.
        
        Args:
            sources: Список источников задач
            
        Returns:
            Dict: Словарь {название_типа_источника: список_задач}
        """
        results: Dict[str, List[Task]] = {}
        
        
        for source in sources:
            try:
                source_name = type(source).__name__
                tasks = self.collect(source)
                
                # Группируем по типу источника
                if source_name not in results:
                    results[source_name] = []
                results[source_name].extend(tasks)
                
                
            except Exception as e:
                print(f"Ошибка при сборе из источника ({type(source).__name__}): {e}")

        

        
        return results
    
    def _resolve_id_conflicts(self, tasks: List[Task]) -> List[Task]:
        resolved_tasks = []
        temp_used = self._used_ids.copy()  # Работаем с копией
        
        for task in tasks:
            if task.id in temp_used:  # Проверяем по временному множеству
                old_id = task.id
                new_id = self._generate_unique_id()
                
                new_task = Task(id=new_id, payload=task.payload)
                resolved_tasks.append(new_task)
                temp_used.add(new_id)  # Добавляем новый ID во временное множество
                
                self._conflicts_count += 1
                print(f"    Конфликт ID {old_id} -> изменен на {new_id}")
            else:
                resolved_tasks.append(task)
                temp_used.add(task.id)  # Добавляем во временное множество
        
        # После обработки всех задач обновляем основное множество
        self._used_ids.update(temp_used)
        return resolved_tasks
    
    def _check_conflicts(self, tasks: List[Task]) -> None:
        """
        Проверяет конфликты ID без исправления (только предупреждает).
        
        Args:
            tasks: Список задач для проверки
        """
        for task in tasks:
            if task.id in self._used_ids:
                print(f"    ВНИМАНИЕ: Конфликт ID {task.id} (задача: {task.payload})")
                self._conflicts_count += 1
            else:
                self._used_ids.add(task.id)
    
    def _generate_unique_id(self) -> int:
        """
        Генерирует уникальный айди.
        
        Returns:
            int: Уникальный ID
        """
        # увеличиваем счетчик, пока не найдем свободный ID
        while self._next_id in self._used_ids:
            self._next_id += 1
        
        unique_id = self._next_id
        self._next_id += 1
        return unique_id
    
    def get_all_tasks(self) -> List[Task]:
        """
        Возвращает все собранные задачи.
        
        Returns:
            List[Task]: Список всех задач
        """
        return self._all_tasks.copy()
    

    
    def print_summary(self) -> None:
        """Выводит сводку о собранных задачах."""
        print("\n" + "="*50)
        print("СВОДКА КОЛЛЕКТОРА")
        print("="*50)
        print(f"Всего собрано задач: {len(self._all_tasks)}")
        print(f"Обнаружено конфликтов ID: {self._conflicts_count}")
        print("==================СПИСОК ЗАДАЧ====================")
        for task in self._all_tasks:
            print(f"ID: {task.id} | payload: {task.payload}")
        print("==================================================")
        
        
    
    def reset(self) -> None:
        """Сбрасывает состояние коллектора (очищает все задачи)."""
        self._all_tasks.clear()
        self._used_ids.clear()
        self._next_id = 1
        self._conflicts_count = 0
        print("Коллектор сброшен")



def quick_collect(sources: List[TaskSourceProtocol]) -> List[Task]:
    
    collector = TaskCollector()
    collector.collect_from_sources(sources)
    return collector.get_all_tasks()


# Функция для демонстрации работы коллектора
def demo_collector():
    """Демонстрирует работу коллектора с разными источниками."""
    from src.task_sources.file_source import FileSource
    from src.task_sources.generator_source import GeneratorSource
    from src.task_sources.API_source import APISource
    
    # Создаем источники
    file_source = FileSource("example.json")
    gen_source = GeneratorSource(count=4, id_start=1)
    api_source = APISource()
    
    
    sources = [file_source, gen_source, api_source]
    
    # Создаем коллектор
    collector = TaskCollector()
    
    # Собираем задачи
    print("Сбор задач...")
    result = collector.collect_from_sources(sources)
    
    # Показываем результат
    all_tasks = collector.get_all_tasks()
    print(all_tasks)

    print("\nСВОДКА:\n")
    collector.print_summary()

    

