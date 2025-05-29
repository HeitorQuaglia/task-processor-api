import logging

from app.services.processor.factory import ProcessorFactory
from app.services.processor.interfaces import IProcessorService
from app.services.processor.service import ProcessorService

logger = logging.getLogger(__name__)

# Re-exportando para compatibilidade com código existente
__all__ = ['ProcessorService', 'IProcessorService', 'default_processor_service']

# Instância default para uso legado
default_processor_service = ProcessorService(ProcessorFactory())