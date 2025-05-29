import logging

from app.repositories.interfaces import ITaskRepository
from app.repositories.mongo_repository import MongoTaskRepository

logger = logging.getLogger(__name__)

# Exporte as classes para manter compatibilidade com código existente
__all__ = ['MongoTaskRepository', 'ITaskRepository']
