import logging

from pydantic.typing import Literal

from app.repositories.task_repository import TaskRepository
from app.models.task_result import TaskResult

logger = logging.getLogger(__name__)

class MongoService:
    @staticmethod
    async def save_task(task: TaskResult):
        """Salva uma nova tarefa no MongoDB."""
        await TaskRepository.save_task_result(task)

    @staticmethod
    async def get_task(task_id: str) -> TaskResult:
        """Recupera uma tarefa pelo ID."""
        return await TaskRepository.get_task_result(task_id)

    @staticmethod
    async def update_task(task_id: str, status: Literal["processing", "error", "completed"], result=None, comment: str = ""):
        """
        Atualiza o status de uma task no MongoDB.
        :param task_id: ID da task a ser atualizada
        :param status: Novo status da task ('processing', 'completed', 'error')
        :param result: Resultado da task (se aplicável)
        :param comment: Comentário ou mensagem sobre o status
        """
        task = await TaskRepository.get_task_result(task_id)

        if not task:
            raise ValueError(f"Tarefa com task_id {task_id} não encontrada.")

        task.status = status
        task.result = result
        task.comment = comment

        await TaskRepository.update_task_result(task)