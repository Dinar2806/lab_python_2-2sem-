from typing import Protocol, runtime_checkable
from src.task.task import Task


@runtime_checkable
class TaskSourceProtocol(Protocol):
    
    def get_tasks(self) -> list[Task]:
        ...
        
        
        

