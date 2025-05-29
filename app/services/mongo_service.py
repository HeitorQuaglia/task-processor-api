import logging
from typing import Literal, Union

from app.services.mongo.factory import TaskServiceFactory
from app.services.mongo.interfaces import ITaskService, TaskStatus

logger = logging.getLogger(__name__)

# Re-exportando para compatibilidade com código existente
__all__ = ['ITaskService', 'TaskStatus', 'default_mongo_service']

# Instância default para uso legado - agora usando a factory
default_mongo_service: ITaskService = TaskServiceFactory.create_mongo_service()