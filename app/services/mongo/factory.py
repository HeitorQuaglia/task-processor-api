"""
Factory para criar serviços de MongoDB.
"""
from app.repositories.mongo_repository import MongoTaskRepository
from app.services.mongo.interfaces import ITaskService
from app.services.mongo.service import TaskService


class TaskServiceFactory:
    """Factory para criar instâncias de serviços de tarefas."""
    
    @staticmethod
    def create_mongo_service() -> ITaskService:
        """Cria um serviço de tarefas usando MongoDB."""
        return TaskService(MongoTaskRepository())
