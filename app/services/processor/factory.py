"""
Factory para processadores de tarefas.
"""
import uuid
import logging
from typing import Dict, Type

from app.models.process_data_input import ProcessDataInput
from app.services.processor.interfaces import IProcessorFactory
from app.services.task_processor.csv_processor import CSVProcessor
from app.services.task_processor.processor import ProcessorProtocol
from app.services.task_processor.url_processor import UrlProcessor

logger = logging.getLogger(__name__)


class ProcessorFactory(IProcessorFactory):
    """Factory para criar processadores."""
    
    def create_processor(self, payload: ProcessDataInput) -> ProcessorProtocol:
        """Cria um processador adequado para o payload."""
        if payload.file:
            return self._create_csv_processor(payload)
        if payload.url is None:
            logger.error("Tentativa de criar processador com URL nula")
            raise ValueError("URL payload cannot be None")
        return self._create_url_processor(payload)
    
    def _create_csv_processor(self, payload: ProcessDataInput) -> ProcessorProtocol:
        """Cria um processador de CSV."""
        logger.info(f"Criando processador CSV para o arquivo: {payload.file.filename}")
        return CSVProcessor(
            task_id=str(uuid.uuid4()),
            payload=payload.file,
            column=int(payload.column) if payload.column is not None else 0
        )
    
    def _create_url_processor(self, payload: ProcessDataInput) -> ProcessorProtocol:
        """Cria um processador de URL."""
        logger.info(f"Criando processador URL para: {payload.url}")
        return UrlProcessor(
            task_id=str(uuid.uuid4()),
            payload=payload.url
        )
