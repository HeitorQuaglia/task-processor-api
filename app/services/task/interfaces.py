"""
Interfaces para os serviços de processamento de tarefas.
"""
from abc import abstractmethod
from typing import Dict, Any, Protocol, Optional, Union

from app.services.mongo_service import TaskStatus


class IUrlValidator(Protocol):
    """Interface para validador de URLs."""
    @abstractmethod
    def validate(self, url: str) -> Dict[str, Any]:
        """Valida uma URL e retorna o resultado."""
        pass


class ICsvProcessor(Protocol):
    """Interface para processador de CSV."""
    @abstractmethod
    def process(self, file_url: str, column_index: int) -> Dict[str, Any]:
        """Processa um arquivo CSV e retorna o resultado."""
        pass


class IBackgroundTaskProcessor(Protocol):
    """Interface para processador de tarefas em background."""
    @abstractmethod
    async def update_task_status(self, task_id: str, status: str, 
                               result: Optional[Union[float, str]] = None, 
                               comment: str = "") -> None:
        """Atualiza o status de uma tarefa."""
        pass
    
    @abstractmethod
    async def validate_url(self, task_id: str, url: str) -> None:
        """Valida uma URL e atualiza o status da tarefa."""
        pass
    
    @abstractmethod
    async def process_csv(self, task_id: str, file_url: str, column_index: int) -> None:
        """Processa um arquivo CSV e atualiza o status da tarefa."""
        pass
