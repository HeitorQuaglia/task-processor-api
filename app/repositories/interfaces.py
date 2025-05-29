"""
Interfaces para os repositórios de dados.
"""
from abc import abstractmethod
from typing import Optional, Protocol

from app.models.task_result import TaskResult


class ITaskReader(Protocol):
    """Interface para leitura de tarefas."""
    @abstractmethod
    async def get_task(self, task_id: str) -> Optional[TaskResult]:
        """Recupera uma tarefa pelo ID."""
        pass


class ITaskWriter(Protocol):
    """Interface para escrita de tarefas."""
    @abstractmethod
    async def save_task(self, task_data: TaskResult) -> None:
        """Salva uma nova tarefa."""
        pass
    
    @abstractmethod
    async def update_task(self, task_data: TaskResult) -> None:
        """Atualiza uma tarefa existente."""
        pass


class ITaskRepository(ITaskReader, ITaskWriter, Protocol):
    """Interface completa para repositório de tarefas."""
    pass
