"""
Interfaces para os processadores de tarefas.
"""
from abc import abstractmethod
from typing import Any, Protocol

from fastapi import BackgroundTasks
from app.models.task_result import TaskResult
from app.services.task_processor.processor_response import ProcessorResponse


class IValidator(Protocol):
    """Interface para validação de dados."""
    @abstractmethod
    def validate(self) -> None:
        """Valida os dados de entrada."""
        pass


class IDataProcessor(Protocol):
    """Interface para processamento de dados."""
    @abstractmethod
    def process(self) -> None:
        """Processa os dados."""
        pass


class ITaskCreator(Protocol):
    """Interface para criação de tarefas."""
    @abstractmethod
    def create_task_data(self) -> TaskResult:
        """Cria os dados da tarefa."""
        pass


class ITaskPersister(Protocol):
    """Interface para persistência de tarefas."""
    @abstractmethod
    async def save_task(self, task_data: TaskResult) -> None:
        """Salva a task no repositório de tasks."""
        pass


class IBackgroundTaskAdder(Protocol):
    """Interface para adição de tarefas em background."""
    @abstractmethod
    def add_background_task(self, background_tasks: BackgroundTasks) -> None:
        """Adiciona uma tarefa em background."""
        pass


class IResponseCreator(Protocol):
    """Interface para criação de respostas."""
    @abstractmethod
    def response(self) -> ProcessorResponse:
        """Cria a resposta do processador."""
        pass


class IProcessorProtocol(IValidator, IDataProcessor, ITaskCreator,
                       ITaskPersister, IBackgroundTaskAdder, IResponseCreator, Protocol):
    """Interface completa para processadores de tarefas."""
    task_id: str
    payload: Any
    
    @abstractmethod
    async def run(self, background_tasks: BackgroundTasks) -> ProcessorResponse:
        """Executa o pipeline de processamento."""
        pass
