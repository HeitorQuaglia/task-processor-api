"""
Interfaces para serviços de MongoDB.
"""
from abc import abstractmethod
from typing import Literal, Optional, Protocol, Union

from app.models.task_result import TaskResult

TaskStatus = Literal["processing", "error", "completed"]


class ITaskService(Protocol):
    """Interface para serviço de tarefas."""
    @abstractmethod
    async def save_task(self, task: TaskResult) -> None:
        """Salva uma nova tarefa."""
        pass

    @abstractmethod
    async def get_task(self, task_id: str) -> TaskResult:
        """Recupera uma tarefa pelo ID."""
        pass

    @abstractmethod
    async def update_task(self, task_id: str, status: TaskStatus, 
                         result: Optional[Union[float, str]] = None, 
                         comment: str = "") -> None:
        """Atualiza o status de uma tarefa existente."""
        pass
