import json
import os

from abc import ABC, abstractmethod
from typing import List
from src.task.task import Task

# Абстрактный класс
class Reader(ABC):
    @abstractmethod
    def get_tasks(self, file_path: str) -> List[Task]:
        """Считывает файл и возвращает список объектов Task"""
        pass
    
    
class FileSource():
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    def get_tasks(self) -> List[Task]:
        extension = os.path.splitext(self.file_path)[1].lower()
        if extension == '.json':
            return self._json_reader(self.file_path)
        
        elif extension == '.txt':
            return self._txt_reader(self.file_path)
        
        else:
            raise ValueError(f"Расширение {extension} не поддерживается, только json и txt")
            
    
    def _json_reader(self, file_path: str) -> List[Task]:
        tasks: List[Task] = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    tasks.append(Task(item["id"], item["payload"]))
        except (json.JSONDecodeError, KeyError) as e:
            raise Exception(f"Ошибка при чтении JSON: {e}")
        
        except FileNotFoundError:
            raise FileNotFoundError("Ошибка: файл json не найден")
        return tasks
    
    def _txt_reader(self, file_path: str) -> List[Task]:
        tasks: List[Task] = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    if ':' not in line:
                        print(f"Ошибка в строке {line_num}: отсутствует ':'")
                        continue
                        
                    task_id, payload = line.split(':', 1)
                    tasks.append(Task(task_id.strip(), payload.strip()))
        except FileNotFoundError:
            raise FileNotFoundError("Ошибка: файл json не найден")
        return tasks
        



            
        
                
        
        