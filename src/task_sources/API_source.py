"""
Модуль содержит источник задач, имитирующий получение данных из API.
Является заглушкой (stub) для демонстрации и тестирования.
"""

import json
import random
from typing import List, Dict, Any, Optional
from datetime import datetime

from src.task.task import Task, TaskStatus


class APISource:
    """
    Заглушка API-источника задач.
    
    Имитирует получение задач из внешнего REST API.
    Не выполняет реальных HTTP-запросов, а возвращает заранее
    подготовленные данные, как будто они пришли с сервера.
    
    Attributes:
        source_name: Название источника (эмулирует разные API)
        response_delay: Имитация задержки сети (в секундах)
        error_rate: Вероятность ошибки (0.0 - 1.0) для имитации сбоев
    """
    
    def __init__(
        self,
        source_name: str = "default",
        response_delay: float = 0.0,
        error_rate: float = 0.0
    ):
        """
        Инициализация API-заглушки.
        
        Args:
            source_name: Название источника (влияет на возвращаемые данные)
            response_delay: Имитация задержки ответа (сек)
            error_rate: Вероятность ошибки (0.0 - 1.0)
        """
        self.source_name = source_name
        self.response_delay = response_delay
        self.error_rate = error_rate
        
        # "База данных" заглушки - разные данные для разных API
        self._mock_database = {
            "default": [
                {"id": 101, "payload": "Задача из API #1", "priority": 5, "status": TaskStatus.TODO},
                {"id": 102, "payload": "Задача из API #2", "priority": 3, "status": TaskStatus.TODO},
                {"id": 103, "payload": "Задача из API #3", "priority": 8, "status": TaskStatus.TODO}
            ],
            "todo": [
            # Здесь priority - int, status храним как строку для удобства мокания
                {"id": 201, "payload": {"title": "Купить продукты"}, "priority": 7, "status": TaskStatus.TODO},
                {"id": 202, "payload": {"title": "Сходить в спортзал"}, "priority": 4, "status": TaskStatus.TODO},
                {"id": 203, "payload": {"title": "Почитать книгу"}, "priority": 1, "status": TaskStatus.TODO}
            ],
            "weather": [
                {"id": 301, "payload": {"city": "Moscow", "temp": -5}, "priority": 2, "status": TaskStatus.IN_PROGRESS},
                {"id": 302, "payload": {"city": "London", "temp": 8}, "priority": 2, "status": TaskStatus.DONE},
            ],
            "empty": [] # Пустой источник для тестирования
        }
    
    def get_tasks(self) -> List[Task]:
        """
        Получает задачи из API-заглушки.
        
        Имитирует поведение реального API:
        - Может "зависать" (response_delay)
        - Может возвращать ошибки (error_rate)
        - Возвращает разные данные в зависимости от source_name
        
        Returns:
            List[Task]: Список задач из "API"
            
        Raises:
            ConnectionError: Если имитируется ошибка сети
            ValueError: Если указан неизвестный источник
        """
        # Имитация случайной ошибки
        if random.random() < self.error_rate:
            raise ConnectionError(f"API {self.source_name} временно недоступен")
        
        # Имитация задержки сети
        if self.response_delay > 0:
            import time
            time.sleep(self.response_delay)
        
        # Получаем данные из "базы" заглушки
        if self.source_name not in self._mock_database:
            raise ValueError(f"Неизвестный источник API: {self.source_name}")
        
        raw_data = self._mock_database[self.source_name]
        
        # Преобразуем сырые данные в объекты Task
        tasks = []
        for item in raw_data:
            task = Task(
                id=item["id"],
                payload=item["payload"],
                priority=item["priority"],
                status=item["status"]
            )
            tasks.append(task)
        
        return tasks
   