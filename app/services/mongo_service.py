from app.repositories.task_repository import TaskRepository
from app.models.task_result import TaskResult

class MongoService:
    @staticmethod
    async def save_task(task: TaskResult):
        """Salva uma nova tarefa no MongoDB."""
        await TaskRepository.save_task_result(task)

    @staticmethod
    async def get_task(task_id: str) -> TaskResult:
        """Recupera uma tarefa pelo ID."""
        return await TaskRepository.get_task_result(task_id)
