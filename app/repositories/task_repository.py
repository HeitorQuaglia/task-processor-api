import logging
from typing import Optional

from app.config.mongo import get_mongo_collection
from app.models.task_result import TaskResult

logger = logging.getLogger(__name__)

class TaskRepository:
    COLLECTION_NAME = "tasks"  # Constante para o nome da coleção

    async def _get_collection(self):
        """Obtém a coleção do MongoDB para tarefas."""
        return await get_mongo_collection(self.COLLECTION_NAME)

    async def save_task(self, task_data: TaskResult):
        """Salva uma nova tarefa no MongoDB."""
        collection = await self._get_collection()
        await collection.insert_one(task_data.dict())

    async def get_task(self, task_id: str) -> Optional[TaskResult]:
        """Obtém o resultado de uma tarefa pelo ID."""
        collection = await self._get_collection()
        task = await collection.find_one({"task_id": task_id})
        if not task:
            return None
        return TaskResult(**task)

    async def update_task(self, task_data: TaskResult):
        """Atualiza uma tarefa existente no MongoDB."""
        collection = await self._get_collection()
        result = await collection.update_one(
            {"task_id": task_data.task_id},
            {"$set": task_data.dict()},
        )
        if result.matched_count == 0:
            raise ValueError(f"No task found with task_id {task_data.task_id}.")
