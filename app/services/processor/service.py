"""
Implementação do serviço de processamento.
"""
import logging

from fastapi import BackgroundTasks

from app.models.process_data_input import ProcessDataInput
from app.services.processor.interfaces import IProcessorFactory, IProcessorService
from app.services.task_processor.processor_response import ProcessorResponse

logger = logging.getLogger(__name__)


class ProcessorService(IProcessorService):
    """Serviço de processamento de dados."""
    
    def __init__(self, processor_factory: IProcessorFactory):
        """Inicializa o serviço com uma factory de processadores."""
        self.processor_factory = processor_factory
    
    async def process_data(self, background_tasks: BackgroundTasks, payload: ProcessDataInput) -> ProcessorResponse:
        """
        Processa os dados recebidos, cria a tarefa no MongoDB e delega a execução ao TaskService.
        """
        logger.info(f"Iniciando processamento de dados: {payload}")
        processor = self.processor_factory.create_processor(payload)
        response = await processor.run(background_tasks)
        logger.info(f"Processamento de dados concluído: {response}")
        return response
