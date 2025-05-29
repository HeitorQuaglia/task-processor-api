"""
Pacote para serviços relacionados ao MongoDB.
"""
from app.services.mongo.interfaces import ITaskService, TaskStatus
from app.services.mongo.service import TaskService
from app.services.mongo.factory import TaskServiceFactory

__all__ = [
    'ITaskService',
    'TaskStatus',
    'TaskService',
    'TaskServiceFactory',
]
