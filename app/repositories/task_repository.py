from app.config.mongo import get_mongo_collection
from app.models.task_result import TaskResult


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
