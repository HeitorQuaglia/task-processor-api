"""
Pacote para serviços relacionados ao processamento de dados.
"""
from app.services.processor.interfaces import IProcessorFactory, IProcessorService
from app.services.processor.factory import ProcessorFactory
from app.services.processor.service import ProcessorService

__all__ = [
    'IProcessorFactory',
    'IProcessorService',
    'ProcessorFactory',
    'ProcessorService',
]
