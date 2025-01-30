import logging

from app.repositories.task_repository import TaskRepository
from app.models.task_result import TaskResult

logger = logging.getLogger(__name__)

from typing import Literal, Optional

TaskStatus = Literal["processing", "error", "completed"]

class MongoService:
    @staticmethod
    async def save_task(task: TaskResult):
        """Salva uma nova tarefa no MongoDB."""
        await TaskRepository.save_task(task)

    @staticmethod
    async def get_task(task_id: str) -> TaskResult:
        """Recupera uma tarefa pelo ID."""
        return await TaskRepository.get_task(task_id)

    @staticmethod
    async def update_task(task_id: str, status: TaskStatus, result: Optional[float | str] = None, comment: str = ""):
        """
        Atualiza o status de uma task no MongoDB.
        :param task_id: ID da task a ser atualizada
        :param status: Novo status da task ('processing', 'completed', 'error')
        :param result: Resultado da task (se aplicável)
        :param comment: Comentário ou mensagem sobre o status
        """
        task = await MongoService._get_task_or_raise(task_id)  # Utilização de função extraída
        task_dict = task.dict()
        task_dict.update({
            "status": status,
            "result": result,
            "comment": comment
        })
        task_updated = TaskResult(**task_dict)
        await TaskRepository.update_task(task_updated)

    @staticmethod
    async def _get_task_or_raise(task_id: str) -> TaskResult:
        """Recupera uma tarefa ou levanta um erro se não existir."""
        task = await TaskRepository.get_task(task_id)
        if not task:
            raise ValueError(f"Tarefa com task_id {task_id} não encontrada.")
        return task