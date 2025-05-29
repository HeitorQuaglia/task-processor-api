"""
Implementação do repositório de tarefas usando MongoDB.
"""
import logging
from typing import Optional

from app.config.mongo import get_mongo_collection
from app.models.task_result import TaskResult
from app.repositories.interfaces import ITaskRepository

logger = logging.getLogger(__name__)


class MongoTaskRepository(ITaskRepository):
    """Implementação do repositório de tarefas usando MongoDB."""
    
    def __init__(self, collection_name: str = "tasks"):
        """Inicializa o repositório com o nome da coleção."""
        self.collection_name = collection_name

    async def _get_collection(self):
        """Obtém a coleção do MongoDB."""
        return await get_mongo_collection(self.collection_name)

    async def save_task(self, task_data: TaskResult) -> None:
        """Salva uma nova tarefa no MongoDB."""
        collection = await self._get_collection()
        await collection.insert_one(task_data.dict())
        logger.info(f"Task {task_data.task_id} saved successfully")

    async def get_task(self, task_id: str) -> Optional[TaskResult]:
        """Recupera uma tarefa pelo ID do MongoDB."""
        collection = await self._get_collection()
        task = await collection.find_one({"task_id": task_id})
        if not task:
            logger.warning(f"Task {task_id} not found")
            return None
        return TaskResult(**task)

    async def update_task(self, task_data: TaskResult) -> None:
        """Atualiza uma tarefa existente no MongoDB."""
        collection = await self._get_collection()
        result = await collection.update_one(
            {"task_id": task_data.task_id},
            {"$set": task_data.dict()},
        )
        if result.matched_count == 0:
            error_msg = f"No task found with task_id {task_data.task_id}."
            logger.error(error_msg)
            raise ValueError(error_msg)
        logger.info(f"Task {task_data.task_id} updated successfully")
