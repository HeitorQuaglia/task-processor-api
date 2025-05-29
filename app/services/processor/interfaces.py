"""
Interfaces para o serviço de processamento.
"""
from abc import abstractmethod
from typing import Protocol

from fastapi import BackgroundTasks

from app.models.process_data_input import ProcessDataInput
from app.services.task_processor.processor import ProcessorProtocol
from app.services.task_processor.processor_response import ProcessorResponse


class IProcessorFactory(Protocol):
    """Interface para factory de processadores."""
    @abstractmethod
    def create_processor(self, payload: ProcessDataInput) -> ProcessorProtocol:
        """Cria um processador adequado para o payload."""
        pass


class IProcessorService(Protocol):
    """Interface para serviço de processamento."""
    @abstractmethod
    async def process_data(self, background_tasks: BackgroundTasks, payload: ProcessDataInput) -> ProcessorResponse:
        """Processa os dados recebidos."""
        pass
