from abc import ABC, abstractmethod
from typing import Any
from fastapi import BackgroundTasks
from app.models.task_result import TaskResult
from app.services.task_processor.processor_response import ProcessorResponse

class ProcessorProtocol(ABC):
    task_id: str
    payload: Any

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def create_task_data(self) -> TaskResult:
        pass

    @abstractmethod
    async def save_task(self, task_data: TaskResult):
        """Salva a task no repositório de tasks."""
        pass

    @abstractmethod
    def add_background_task(self, background_tasks: BackgroundTasks):
        pass


    @abstractmethod
    def response(self) -> 'ProcessorResponse':
        pass

    async def run(self, background_tasks: BackgroundTasks) -> 'ProcessorResponse':
        """
        Executa o pipeline padrão de processamento:
        1. Valida entrada
        2. Processa dados
        3. Cria estrutura da task
        4. Salva no banco
        5. Adiciona tarefa em background
        6. Retorna resposta
        """
        self.validate()
        self.process()
        task_data = self.create_task_data()
        await self.save_task(task_data)
        self.add_background_task(background_tasks)
        return self.response()
