import random
from typing import Any, Union, List
from src.task.task import Task, TaskStatus


class GeneratorSource():
    
    def __init__(self, count: int = 5, id_start: int = 0):
        """
            Инициализация генератора
        Args:
            count (int, optional): _description_. Defaults to 5.
            id_start (int, optional): _description_. Defaults to 0.
            payload_type (str, optional): _description_. Defaults to "text".
        """
        
        if count <= 0:
            raise ValueError("Количество задач должно быть положительным числом")
        
  
        
        self.count = count
        self.id_start = id_start
        
    def get_tasks(self) -> List[Task]:
        """
        Генерация списка задач

        Returns:
            List[Task]: _description_
        """
        
        tasks = []
        
        for i in range(self.count):
            task_id = self.id_start + i
            
            payload = self._generate_text_payload(i)
            status = TaskStatus.TODO
            priority = random.randint(1, 10)
           
                
            task = Task(id=task_id, payload=payload, status=status, priority=priority)
            tasks.append(task)
        
        return tasks
                
        
    
    def _generate_text_payload(self, index: int) -> str:
        """Генерация полезного содержания payload для Task

        Args:
            index (int): _description_

        Returns:
            str: _description_
        """
        
        texts = [
            f"Убрать мусор в комнате {random.randint(1,500)}",
            f"Вымыть полы в комнате {random.randint(1,500)}",
            f"Отправить отчет №{index}",
            f"Позвонить клиенту {index}",
            f"Написать письмо {index}",
            f"Проверить документы {index}",
            f"Сделать резервную копию {index}"
        ]
        
        return random.choice(texts)
    

                
                

                
        