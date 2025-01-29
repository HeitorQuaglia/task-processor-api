import logging

from app.config.mongo import get_mongo_collection
from app.models.task_result import TaskResult

logger = logging.getLogger(__name__)

class TaskRepository:
    @staticmethod
    async def save_task_result(task_data: TaskResult):
        collection = await get_mongo_collection("tasks")
        await collection.insert_one(task_data.dict())

    @staticmethod
    async def get_task_result(task_id: str) -> TaskResult:
        collection = await get_mongo_collection("tasks")
        task = await collection.find_one({"task_id": task_id})

        if not task:
            return None

        return TaskResult(**task)


    @staticmethod
    async def update_task_result(task_data: TaskResult):
        """Atualiza uma tarefa existente no MongoDB."""
        collection = await get_mongo_collection("tasks")

        result = await collection.update_one(
            {"task_id": task_data.task_id},
            {"$set": task_data.dict()},
        )

        if result.matched_count == 0:
            raise ValueError(f"No task found with task_id {task_data.task_id}.")
